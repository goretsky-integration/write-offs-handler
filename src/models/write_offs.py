import datetime

from pydantic import BaseModel, constr, validator

from models.ingredients import Ingredient


def to_naive_datetime(value: str) -> str:
    return value.split('+')[0].rstrip('Z')


class WriteOffIn(BaseModel):
    unit_name: constr(min_length=2, max_length=255)
    ingredient_name: constr(min_length=2, max_length=255)
    to_be_write_off_at: datetime.datetime

    _to_naive_datetime = validator('to_be_write_off_at', allow_reuse=True, pre=True)(to_naive_datetime)


class WriteOff(BaseModel):
    id: int
    unit_id: int
    ingredient: Ingredient
    to_be_write_off_at: datetime.datetime
    written_off_at: datetime.datetime | None


class WrittenOffAtIn(BaseModel):
    written_off_at: datetime.datetime | None

    _to_naive_datetime = validator('written_off_at', allow_reuse=True, pre=True)(to_naive_datetime)
