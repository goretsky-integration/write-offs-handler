import asyncio
import collections
import uuid

from fastapi import APIRouter, status
from fastapi.params import Depends
from sse_starlette import EventSourceResponse, ServerSentEvent

import models
from api.dependencies import get_event_channels
from resources.events import get_ping_message
from services import logger
from services.database_api import Units
from services.event_channels import EventChannels

router = APIRouter(prefix='/events', tags=['Events'])


async def gen(event_channels: EventChannels, request_uuid: uuid.UUID, delay: int = 10):
    await event_channels.subscribe(request_uuid)
    try:
        while True:
            event = await event_channels.get_event_or_none(request_uuid)
            if event is not None:
                yield ServerSentEvent(
                    data=event.data.json(ensure_ascii=False),
                    event=event.event_type.name,
                    id=str(event.id)
                )
            await asyncio.sleep(delay)
    except asyncio.CancelledError as error:
        # async code here won't be executed, so unsubscribe method is not async
        event_channels.unsubscribe(request_uuid)
        raise error


@router.get(
    path='/',
    status_code=status.HTTP_207_MULTI_STATUS,
)
async def events_stream(
        request_uuid: uuid.UUID = Depends(uuid.uuid4),
        event_channels: EventChannels = Depends(get_event_channels),
):
    return EventSourceResponse(
        content=gen(event_channels, request_uuid),
        ping_message_factory=get_ping_message,
    )


@router.post('/')
async def create_events(
        worksheets_events: list[models.WorksheetEvents],
        event_channels: EventChannels = Depends(get_event_channels),
):
    errors = collections.defaultdict(list)
    for worksheet_events in worksheets_events:
        try:
            unit = await Units.get_by_name(worksheet_events.worksheet_name)
        except KeyError:
            errors['unit_names'].append(worksheet_events.worksheet_name)
            logger.warning(f'Invalid unit name {worksheet_events.worksheet_name}')
        else:
            for event in worksheet_events.events:
                await event_channels.broadcast(models.Event(data={'unit_id': unit.id, 'unit_name': unit.name},
                                                            event_type=event))
                logger.debug(f'New event {event.name} {unit.name}')
    return {'errors': errors}
