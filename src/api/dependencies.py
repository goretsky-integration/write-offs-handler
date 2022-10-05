from db import redis_db
from db.engine import session_maker
from repositories import WriteOffRepository, IngredientRepository
from services.event_channels import EventChannels

__all__ = (
    'get_event_channels',
    'get_write_offs_repository',
    'get_ingredients_repository',
)


def get_event_channels() -> EventChannels:
    return EventChannels(redis_db.redis_sync, redis_db.redis_async)


def get_write_offs_repository() -> WriteOffRepository:
    return WriteOffRepository(session_maker)


def get_ingredients_repository() -> IngredientRepository:
    return IngredientRepository(session_maker)
