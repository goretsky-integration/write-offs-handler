import datetime

from pydantic import BaseModel, constr, validator

from models.ingredients import Ingredient


def to_naive_datetime(value: str | None) -> str | None:
    if isinstance(value, str):
        return value.split('+')[0].rstrip('Z')


class WriteOffIn(BaseModel):
    unit_name: constr(min_length=2, max_length=255)
    ingredient_name: constr(min_length=2, max_length=255)
    to_be_write_off_at: datetime.datetime

    _to_naive_datetime = validator('to_be_write_off_at', allow_reuse=True, pre=True)(to_naive_datetime)


class WriteOff(BaseModel):
    id: int
    unit_id: int
    ingredient_name: str
    to_be_write_off_at: datetime.datetime
    written_off_at: datetime.datetime | None

    _to_naive_datetime = validator('written_off_at', 'written_off_at', allow_reuse=True, pre=True)(to_naive_datetime)


class WrittenOffAtIn(BaseModel):
    written_off_at: datetime.datetime | None

    _to_naive_datetime = validator('written_off_at', allow_reuse=True, pre=True)(to_naive_datetime)
