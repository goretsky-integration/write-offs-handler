from db import redis_db
from services.event_channels import EventChannels

__all__ = (
    'get_event_channels',
)


def get_event_channels() -> EventChannels:
    return EventChannels(redis_db.redis_sync, redis_db.redis_async)
