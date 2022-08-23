import asyncio
import json
import uuid

from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from sse_starlette import EventSourceResponse, ServerSentEvent

import models
from api.dependencies import get_event_channels
from resources.events import get_ping_message
from services.event_channels import EventChannels

router = APIRouter(prefix='/events')


async def gen(event_channels: EventChannels, request_uuid: uuid.UUID, delay: int = 10):
    await event_channels.subscribe(request_uuid)
    try:
        while True:
            event = await event_channels.get_event_or_none(request_uuid)
            if event is not None:
                yield ServerSentEvent(
                    data=event.data.json(),
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


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
        event: models.Event,
        event_channels: EventChannels = Depends(get_event_channels),
):
    await event_channels.broadcast(event)
    return Response(status_code=status.HTTP_201_CREATED)
