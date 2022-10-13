from pydantic import BaseModel, Field, PositiveInt, constr

import models

__all__ = (
    'WorksheetEvents',
    'UnitEvents',
)


class UnitEvents(BaseModel):
    unit_id: PositiveInt
    unit_name: constr(min_length=2, max_length=255)
    events: set[models.EventType]


class WorksheetEvents(BaseModel):
    worksheet_name: str = Field(alias='worksheetName')
    events: list[models.EventType]
