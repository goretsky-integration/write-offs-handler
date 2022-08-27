from pydantic import BaseModel, Field

import models

__all__ = (
    'WorksheetEvents',
)


class WorksheetEvents(BaseModel):
    worksheet_name: str = Field(alias='worksheetName')
    events: list[models.EventType]
