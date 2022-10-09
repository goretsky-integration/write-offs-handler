import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

import exceptions
import models
from db.models import WriteOff, Ingredient
from repositories.base import BaseRepository


class WriteOffRepository(BaseRepository):

    async def create(self, unit_id: int, write_off_in: models.WriteOffIn, ingredient) -> models.WriteOff:
        write_off = WriteOff(unit_id=unit_id,
                             ingredient_id=ingredient.id,
                             to_be_write_off_at=write_off_in.to_be_write_off_at)
        async with (
            self._session_maker() as session,
            session.begin(),
        ):
            session.add(write_off)

        return models.WriteOff(
            id=write_off.id,
            unit_id=write_off.unit_id,
            to_be_write_off_at=write_off.to_be_write_off_at,
            written_off_at=write_off.written_off_at,
            ingredient_name=ingredient.name,
        )

    async def get_by_id(self, write_off_id: int) -> models.WriteOff:
        statement = (select(WriteOff)
                     .join(Ingredient)
                     .options(joinedload(WriteOff.ingredient))
                     .where(Ingredient.id == write_off_id))
        async with self._session_maker() as session:
            result = await session.execute(statement)
        write_off = result.scalar()
        if write_off is None:
            raise exceptions.DoesNotExist

        return models.WriteOff(
            id=write_off.id,
            unit_id=write_off.unit_id,
            to_be_write_off_at=write_off.to_be_write_off_at,
            written_off_at=write_off.written_off_at,
            ingredient_name=write_off.ingredient.name,
        )

    async def get_by_unit_id_and_ingredient_name(self, unit_id: int, ingredient_name: str) -> models.WriteOff:
        statement = (select(WriteOff)
                     .join(Ingredient)
                     .options(joinedload(WriteOff.ingredient))
                     .where(Ingredient.name == ingredient_name, WriteOff.unit_id == unit_id))

        async with self._session_maker() as session:
            result = await session.execute(statement)

        write_off = result.scalar()
        if write_off is None:
            raise exceptions.DoesNotExist

        return models.WriteOff(
            id=write_off.id,
            unit_id=write_off.unit_id,
            to_be_write_off_at=write_off.to_be_write_off_at,
            written_off_at=write_off.written_off_at,
            ingredient_name=write_off.ingredient.name,
        )

    async def update_written_off_at(self, write_off_id: int, written_off_at_in: models.WrittenOffAtIn):
        statement = (update(WriteOff)
                     .values(written_off_at=written_off_at_in.written_off_at)
                     .where(WriteOff.id == write_off_id))

        async with (
            self._session_maker() as session,
            session.begin()
        ):
            result = await session.execute(statement)
        if not result.rowcount:
            raise exceptions.IsNotUpdated

    async def get_py_period(
            self,
            from_datetime: datetime.datetime,
            to_datetime: datetime.datetime,
    ) -> list[models.WriteOff]:
        statement = (select(WriteOff)
                     .options(joinedload(WriteOff.ingredient))
                     .where(WriteOff.to_be_write_off_at >= from_datetime,
                            WriteOff.to_be_write_off_at <= to_datetime))
        async with self._session_maker() as session:
            result = await session.execute(statement)

        return [models.WriteOff(id=write_off.id,
                                unit_id=write_off.unit_id,
                                ingredient_name=write_off.ingredient.name,
                                to_be_write_off_at=write_off.to_be_write_off_at,
                                written_off_at=write_off.written_off_at)
                for write_off in result.scalars()]
