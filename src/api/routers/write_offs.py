from fastapi import APIRouter, Response, status, Depends

from api import schemas, dependencies
from repositories import WriteOffRepository
from services.external_database import ExternalDatabaseService

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
)
def create_write_off(
        write_off: schemas.WriteOffCreate,
        write_offs: WriteOffRepository = Depends(dependencies.get_write_offs_repository),
        external_database_service: ExternalDatabaseService = Depends(dependencies.get_external_database_service),
):
    unit = external_database_service.get_units(name=write_off.unit_name)
    write_offs.create(
        unit_id=unit.id,
        ingredient_name=write_off.ingredient_name,
        to_be_written_off_at=write_off.to_be_written_off_at,
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    path='/unit/{unit_name}/ingredient/{ingredient_name}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_write_off(
        unit_name: schemas.UnitName,
        ingredient_name: schemas.IngredientName,
):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
