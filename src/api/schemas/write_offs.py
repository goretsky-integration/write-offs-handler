import datetime
from typing import TypeAlias

from pydantic import BaseModel, constr, Field

__all__ = (
    'UnitName',
    'IngredientName',
    'ToBeWrittenOffAt',
    'WriteOffCreate',
    'WriteOffUpdate',
)

UnitName: TypeAlias = constr(min_length=1, max_length=64)
IngredientName: TypeAlias = constr(min_length=1, max_length=255)
ToBeWrittenOffAt: TypeAlias = datetime.datetime


class WriteOffCreate(BaseModel):
    unit_name: UnitName = Field(alias='unitName')
    ingredient_name: IngredientName = Field(alias='ingredientName')
    to_be_written_off_at: ToBeWrittenOffAt = Field(alias='toBeWrittenOffAt')


class WriteOffUpdate(BaseModel):
    unit_name: UnitName = Field(alias='unitName')
    ingredient_name: IngredientName = Field(alias='ingredientName')
    to_be_written_off_at: ToBeWrittenOffAt = Field(alias='toBeWrittenOffAt')
    is_written_off: bool
