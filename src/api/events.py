from fastapi import APIRouter
from fastapi.params import Depends
from pika.adapters.blocking_connection import BlockingChannel

import models
from db import message_queue
from db.message_queue import get_message_queue_channel

router = APIRouter(prefix='/events', tags=['Events'])


def prepare_message_body(unit_id: int, unit_name: str, event_type: str) -> dict:
    return {
        'type': 'WRITE_OFFS',
        'unit_id': unit_id,
        'payload': {
            'event_type': event_type,
            'unit_name': unit_name,
        },
    }


@router.post('/')
def create_events(
        units_events: list[models.UnitEvents],
):
    with get_message_queue_channel() as channel:
        for unit_events in units_events:
            for event in unit_events.events:
                body = prepare_message_body(unit_events.unit_id, unit_events.unit_name, event.name)
                message_queue.send_json_message(channel, body)
