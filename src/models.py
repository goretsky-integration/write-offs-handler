from enum import Enum

from pydantic import BaseModel, PositiveInt, constr

__all__ = (
    'UnitEvents',
    'EventType',
    'Event',
)


class EventType(Enum):
    EXPIRE_AT_15_MINUTES = 'EXPIRE_AT_15_MINUTES'
    EXPIRE_AT_10_MINUTES = 'EXPIRE_AT_10_MINUTES'
    EXPIRE_AT_5_MINUTES = 'EXPIRE_AT_5_MINUTES'
    ALREADY_EXPIRED = 'ALREADY_EXPIRED'


class Event(BaseModel):
    type: EventType
    ingredient_name: str


class UnitEvents(BaseModel):
    unit_id: PositiveInt
    unit_name: constr(min_length=2, max_length=255)
    events: list[Event]
