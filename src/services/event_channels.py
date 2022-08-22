import asyncio
from uuid import UUID

import redis

import models

__all__ = (
    'EventChannels',
)


class EventChannels:
    channel_keys = 'CHANNEL-KEYS'

    __slots__ = ('__redis_async', '__redis_sync',)

    def __init__(self, redis_sync: redis.Redis, redis_async):
        self.__redis_async = redis_async
        self.__redis_sync = redis_sync

    async def get_channel_keys(self) -> set[str]:
        return await self.__redis_async.smembers(self.channel_keys)

    async def broadcast(self, event: models.Event):
        channel_keys = await self.get_channel_keys()
        event = event.json(by_alias=True)
        tasks = (self.__redis_async.sadd(channel_key, event) for channel_key in channel_keys)
        await asyncio.gather(*tasks)

    def unsubscribe(self, request_uuid: UUID):
        self.__redis_sync.srem(self.channel_keys, request_uuid.hex)
        self.__redis_sync.delete(request_uuid.hex)

    async def subscribe(self, request_uuid: UUID):
        await self.__redis_async.sadd(self.channel_keys, request_uuid.hex)

    async def get_event_or_none(self, request_uuid: UUID) -> models.Event | None:
        event = await self.__redis_async.spop(request_uuid.hex)
        if event:
            return models.Event.parse_raw(event)
