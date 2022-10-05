from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import constr, conint, PositiveInt, NonNegativeInt

import exceptions
import models
from api.dependencies import get_ingredients_repository
from repositories import IngredientRepository

router = APIRouter(prefix='/ingredients', tags=['Ingredients'])


@router.get(
    path='/{ingredient_id}/',
    response_model=models.Ingredient,
)
async def get_ingredient_by_id(
        ingredient_id: PositiveInt,
        ingredients: IngredientRepository = Depends(get_ingredients_repository),
):
    try:
        return await ingredients.get_by_id(ingredient_id)
    except exceptions.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail={'error': f'Ingredient by id "{ingredient_id}" is not found'})


@router.get(
    path='/name/{ingredient_name}/',
    response_model=models.Ingredient,
)
async def get_ingredient_by_name(
        ingredient_name: constr(max_length=255, min_length=2),
        ingredients: IngredientRepository = Depends(get_ingredients_repository),
):
    try:
        return await ingredients.get_by_name(ingredient_name)
    except exceptions.DoesNotExist:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail={'error': f'Ingredient by name "{ingredient_name}" is not found'})


@router.get(
    path='/',
    response_model=list[models.Ingredient],
)
async def get_all_ingredients(
        limit: conint(ge=1, le=1000) = 50,
        offset: NonNegativeInt = 0,
        ingredients: IngredientRepository = Depends(get_ingredients_repository),
):
    return await ingredients.get_all(limit, offset)


@router.post(
    path='/',
    response_model=models.Ingredient,
)
async def create_ingredient(
        ingredient_in: models.IngredientIn,
        ingredients: IngredientRepository = Depends(get_ingredients_repository),
):
    try:
        created_ingredient = await ingredients.create(ingredient_in)
    except exceptions.AlreadyExists:
        raise HTTPException(status.HTTP_409_CONFLICT, detail={'error': 'Ingredient already exists'})
    return created_ingredient
