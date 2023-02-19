import httpx

import exceptions
import models

__all__ = ('ExternalDatabaseService',)


class ExternalDatabaseService:

    def __init__(self, *, base_url: str):
        self.__base_url = base_url

    def get_unit_by_name(self, *, name: str) -> models.Unit:
        url = f'{self.__base_url}/units/name/{name}/'
        response = httpx.get(url)
        if response.status_code == 404:
            raise exceptions.UnitNotFound
        return models.Unit.parse_obj(response.json())
