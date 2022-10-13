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
        logger.debug(f'request {request_uuid} unsubscribed')
        raise error


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
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
        units_events: list[models.UnitEvents],
        event_channels: EventChannels = Depends(get_event_channels),
):
    for unit_events in units_events:
        data = {'unit_id': unit_events.unit_id, 'unit_name': unit_events.unit_name}
        for event in unit_events.events:
            await event_channels.broadcast(models.Event(data=data,
                                                        event_type=event))
            logger.debug(f'New event {unit_events}')
