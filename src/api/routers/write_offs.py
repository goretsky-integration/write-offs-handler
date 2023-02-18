from fastapi import APIRouter, Response, status

from api import schemas

router = APIRouter()


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
)
def create_write_off(
        write_off: schemas.WriteOffCreate,
):
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


@router.patch(
    path='/unit/{unit_name}/ingredient/{ingredient_name}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_write_off(
        unit_name: schemas.UnitName,
        ingredient_name: schemas.IngredientName,
        write_off: schemas.WriteOffUpdate,
):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
