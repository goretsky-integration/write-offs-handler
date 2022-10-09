import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import PositiveInt, constr

import exceptions
import models
from api.dependencies import get_write_offs_repository, get_ingredients_repository
from repositories import WriteOffRepository, IngredientRepository
from services.database_api import Units

router = APIRouter(prefix='/write-offs', tags=['Write offs'])


@router.get(
    path='/{write_off_id}/',
    response_model=models.WriteOff,
)
async def get_write_off_by_id(
        write_off_id: PositiveInt,
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    try:
        return await write_offs.get_by_id(write_off_id)
    except exceptions.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={'error': 'Write off by id is not found'})


@router.get(
    path='/units/{unit_id}/ingredients/{ingredient_name}/',
    response_model=models.WriteOff,
)
async def get_write_off_by_unit_id_and_ingredient_name(
        unit_id: PositiveInt,
        ingredient_name: constr(min_length=2, max_length=255),
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    try:
        return await write_offs.get_by_unit_id_and_ingredient_name(unit_id, ingredient_name)
    except exceptions.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={'error': 'Write off is not found'})


@router.get(
    path='/',
    response_model=list[models.WriteOff],
)
async def get_write_offs(
        from_datetime: datetime.datetime | None,
        to_datetime: datetime.datetime | None,
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    return await write_offs.get_py_period(from_datetime, to_datetime)


@router.post(
    path='/',
)
async def create_write_off(
        write_off_in: models.WriteOffIn,
        ingredients: IngredientRepository = Depends(get_ingredients_repository),
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    try:
        unit = await Units.get_by_name(write_off_in.unit_name)
    except KeyError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={'error': 'Unit by name is not found'})
    ingredient, _ = await ingredients.get_or_create(write_off_in.ingredient_name)
    return await write_offs.create(unit.id, write_off_in, ingredient)


@router.patch(
    path='/{write_off_id}/',
)
async def set_as_written_off(
        write_off_id: PositiveInt,
        written_off_at_in: models.WrittenOffAtIn,
        write_offs: WriteOffRepository = Depends(get_write_offs_repository),
):
    try:
        return await write_offs.update_written_off_at(write_off_id, written_off_at_in)
    except exceptions.IsNotUpdated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail={'error': 'Nothing to update'})
