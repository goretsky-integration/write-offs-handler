from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

import message_queue
import models
from dependencies import TokenBearer
from message_queue import get_message_queue_channel
from settings import get_app_settings

router = APIRouter(prefix='/events', tags=['Events'])


def validate_token(token: str) -> None:
    if token != get_app_settings().token:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid token')


@router.post('/')
def create_events(
        units_events: list[models.UnitEvents],
        token: str = Depends(TokenBearer()),
):
    validate_token(token)
    logger.info(f'Event {units_events}')
    with get_message_queue_channel() as channel:
        for unit_events in units_events:
            for event in unit_events.events:
                body = message_queue.prepare_message_body(unit_events.unit_id, unit_events.unit_name,
                                                          event.type.name, event.ingredient_name)
                message_queue.send_json_message(channel, body)
