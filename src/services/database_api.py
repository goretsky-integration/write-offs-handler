from dodolib import DatabaseClient
from dodolib.models import Unit

from services.logger import logger

__all__ = (
    'Units',
)


class Units:
    unit_name_to_unit = dict()

    @classmethod
    async def get_by_name(cls, name: str) -> Unit:
        if name not in cls.unit_name_to_unit:
            logger.debug('Request to the server')
            units = await cls.get_from_api()
            cls.unit_name_to_unit = {unit.name: unit for unit in units}
        return cls.unit_name_to_unit[name]

    @staticmethod
    async def get_from_api() -> list[Unit]:
        async with DatabaseClient() as client:
            return await client.get_units()
