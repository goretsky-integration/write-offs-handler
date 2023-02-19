import datetime
from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel

__all__ = ('Unit', 'WriteOffInDatabaseDTO')


class Unit(BaseModel):
    id: int
    name: str
    uuid: UUID
    account_name: str
    region: str


@dataclass(frozen=True, slots=True)
class WriteOffInDatabaseDTO:
    unit_id: int
    ingredient_name: str
    to_be_written_off_at: datetime.datetime
