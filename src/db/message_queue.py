import contextlib
import json

import pika.exceptions
from pika.adapters.blocking_connection import BlockingChannel

from settings import get_rabbitmq_settings


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
