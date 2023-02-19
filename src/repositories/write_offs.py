import datetime

from sqlalchemy import delete, select

import models
from database.models import WriteOff
from repositories.base import Repository

__all__ = ('WriteOffRepository',)


class WriteOffRepository(Repository):

    def get_by_unit_id(
            self,
            unit_id: int,
            *,
            limit: int | None = None,
            offset: int | None = None,
    ) -> list[models.WriteOffInDatabaseDTO]:
        statement = (
            select(WriteOff)
            .where(WriteOff.unit_id == unit_id)
            .order_by(WriteOff.to_be_written_off_at.desc())
        )
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
        with self._session_factory() as session:
            write_offs = session.scalars(statement)
            return [
                models.WriteOffInDatabaseDTO(
                    unit_id=write_off.unit_id,
                    ingredient_name=write_off.ingredient_name,
                    to_be_written_off_at=write_off.to_be_written_off_at,
                ) for write_off in write_offs
            ]

    def create(self, *, unit_id: int, ingredient_name: str, to_be_written_off_at: datetime.datetime) -> None:
        write_off = WriteOff(
            unit_id=unit_id,
            ingredient_name=ingredient_name,
            to_be_written_off_at=to_be_written_off_at,
        )
        with self._session_factory() as session:
            with session.begin():
                session.add(write_off)

    def remove(self, *, unit_id: int, ingredient_name: str) -> bool:
        statement = (
            delete(WriteOff)
            .where(WriteOff.unit_id == unit_id, WriteOff.ingredient_name == ingredient_name)
        )
        with self._session_factory() as session:
            with session.begin():
                result = session.execute(statement)
        return bool(result.rowcount)
