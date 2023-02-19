import datetime
from typing import TypeAlias

from pydantic import BaseModel, constr, Field, validator

__all__ = (
    'UnitName',
    'IngredientName',
    'ToBeWrittenOffAt',
    'WriteOff',
    'WriteOffCreate',
    'PaginatedWriteOffs',
)

UnitName: TypeAlias = constr(min_length=1, max_length=64)
IngredientName: TypeAlias = constr(min_length=1, max_length=255)
ToBeWrittenOffAt: TypeAlias = datetime.datetime


class WriteOff(BaseModel):
    unit_name: UnitName = Field(example='Москва 4-1')
    ingredient_name: IngredientName = Field(example='Тесто 35')
    to_be_written_off_at: ToBeWrittenOffAt = Field(example='2023-02-19T06:51:59')


class PaginatedWriteOffs(BaseModel):
    write_offs: list[WriteOff]
    is_end_of_list_reached: bool


class WriteOffCreate(BaseModel):
    unit_name: UnitName = Field(alias='unitName', example='Москва 4-1')
    ingredient_name: IngredientName = Field(alias='ingredientName', example='Тесто 35')
    to_be_written_off_at: ToBeWrittenOffAt = Field(alias='toBeWrittenOffAt', example='2023-02-19T06:51:59')

    @validator('to_be_written_off_at')
    def write_off_time_greater_than_now(cls, v: datetime.datetime) -> datetime.datetime:
        now = datetime.datetime.utcnow()
        if now >= v:
            raise ValueError('Write off time must be greater than now (UTC time)')
        return v
