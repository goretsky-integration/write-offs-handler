import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

__all__ = (
    'Event',
    'EventType',
)


class EventType(Enum):
    EXPIRE_AT_15_MINUTES = 'EXPIRE_AT_15_MINUTES'
    EXPIRE_AT_10_MINUTES = 'EXPIRE_AT_10_MINUTES'
    EXPIRE_AT_5_MINUTES = 'EXPIRE_AT_5_MINUTES'
    ALREADY_EXPIRED = 'ALREADY_EXPIRED'


class EventData(BaseModel):
    unit_id: int
    write_off_at: datetime.datetime


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    data: EventData
    event_type: EventType = Field(alias='event')

    class Config:
        allow_population_by_field_name = True
