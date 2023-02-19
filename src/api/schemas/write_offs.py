import datetime
from typing import TypeAlias

from pydantic import BaseModel, constr, Field, validator

__all__ = (
    'UnitName',
    'IngredientName',
    'ToBeWrittenOffAt',
    'WriteOffCreate',
)

UnitName: TypeAlias = constr(min_length=1, max_length=64)
IngredientName: TypeAlias = constr(min_length=1, max_length=255)
ToBeWrittenOffAt: TypeAlias = datetime.datetime


class WriteOffCreate(BaseModel):
    unit_name: UnitName = Field(alias='unitName')
    ingredient_name: IngredientName = Field(alias='ingredientName')
    to_be_written_off_at: ToBeWrittenOffAt = Field(alias='toBeWrittenOffAt')

    @validator('to_be_written_off_at')
    def write_off_time_greater_than_now(cls, v: datetime.datetime) -> datetime.datetime:
        now = datetime.datetime.utcnow()
        if now >= v:
            raise ValueError('Write off time must be greater than now (UTC time)')
        return v
