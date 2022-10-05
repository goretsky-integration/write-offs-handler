from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

import exceptions
import models
from repositories.base import BaseRepository
from db.models import Ingredient

__all__ = (
    'IngredientRepository',
)


class IngredientRepository(BaseRepository):

    async def create(self, ingredient_in: models.IngredientIn) -> models.Ingredient:
        ingredient = Ingredient(name=ingredient_in.name)
        try:
            async with (
                self._session_maker() as session,
                session.begin(),
            ):
                session.add(ingredient)
        except IntegrityError:
            raise exceptions.AlreadyExists
        return models.Ingredient(id=ingredient.id, name=ingredient.name)

    async def get_by_name(self, ingredient_name: str) -> models.Ingredient:
        statement = select(Ingredient).where(Ingredient.name == ingredient_name)
        async with self._session_maker() as session:
            result = await session.execute(statement)
        ingredient = result.scalar()
        if ingredient is None:
            raise exceptions.DoesNotExist
        return models.Ingredient(id=ingredient.id, name=ingredient.name)

    async def get_by_id(self, ingredient_id: int) -> models.Ingredient:
        statement = select(Ingredient).where(Ingredient.id == ingredient_id)
        async with self._session_maker() as session:
            result = await session.execute(statement)
        ingredient = result.scalar()
        if ingredient is None:
            raise exceptions.DoesNotExist
        return models.Ingredient(id=ingredient.id, name=ingredient.name)

    async def get_all(self, limit: int, offset: int) -> list[models.Ingredient]:
        statement = select(Ingredient).limit(limit).offset(offset)
        async with self._session_maker() as session:
            result = await session.execute(statement)
        return [models.Ingredient(id=ingredient.id, name=ingredient.name) for ingredient in result.scalars()]
