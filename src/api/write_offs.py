import datetime

from fastapi import APIRouter, Depends
from pydantic import constr

import models
from api.dependencies import get_write_offs_repository
from repositories import WriteOffRepository

router = APIRouter(prefix='/write-offs')


@router.get(
    path='/',
    response_model=list[models.WriteOff],
)
async def get_write_offs(
        from_datetime: datetime.datetime | None,
        to_datetime: datetime.datetime | None,
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    return write_offs.get(from_datetime, to_datetime)


@router.post(
    path='/',
)
def create_write_off(
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    return


@router.patch(
    path='/{write_off_id}/'
)
async def set_as_written_off(
        write_off_id: int
):
    pass
