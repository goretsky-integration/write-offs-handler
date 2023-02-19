import datetime

from sqlalchemy import delete

from database.models import WriteOff
from repositories.base import Repository

__all__ = ('WriteOffRepository',)


class WriteOffRepository(Repository):

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
