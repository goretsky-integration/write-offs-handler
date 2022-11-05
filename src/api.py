from fastapi import APIRouter

import message_queue
import models
from message_queue import get_message_queue_channel

router = APIRouter(prefix='/events', tags=['Events'])


@router.post('/')
def create_events(units_events: list[models.UnitEvents]):
    with get_message_queue_channel() as channel:
        for unit_events in units_events:
            for event in unit_events.events:
                body = message_queue.prepare_message_body(unit_events.unit_id, unit_events.unit_name, event.name)
                message_queue.send_json_message(channel, body)
