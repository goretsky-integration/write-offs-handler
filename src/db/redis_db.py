import redis as redis_sync
import redis.asyncio as redis_async

import settings

__all__ = (
    'redis_async',
    'redis_sync',
)

redis_sync = redis_sync.from_url(settings.get_redis_settings().url, decode_responses=True)
redis_async = redis_async.from_url(settings.get_redis_settings().url, decode_responses=True)
