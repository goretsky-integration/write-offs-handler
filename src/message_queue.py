import contextlib
import json

import pika.exceptions
from pika.adapters.blocking_connection import BlockingChannel

from settings import get_rabbitmq_settings

__all__ = (
    'get_message_queue_channel',
    'send_json_message',
    'prepare_message_body',
)


@contextlib.contextmanager
def get_message_queue_channel() -> BlockingChannel:
    parameters = pika.URLParameters(get_rabbitmq_settings().url)
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        channel.queue_declare('telegram-notifications')
        yield channel


def send_json_message(channel: BlockingChannel, data: dict):
    channel.basic_publish(
        exchange='',
        routing_key='telegram-notifications',
        body=json.dumps(data, default=str).encode('utf-8'),
    )


def prepare_message_body(unit_id: int, unit_name: str, event_type: str) -> dict:
    return {
        'type': 'WRITE_OFFS',
        'unit_id': unit_id,
        'payload': {
            'event_type': event_type,
            'unit_name': unit_name,
        },
    }
