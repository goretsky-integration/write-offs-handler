from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import sessionmaker

from database.engine import engine
from repositories import WriteOffRepository
from services.external_database import ExternalDatabaseService
from settings import settings

__all__ = (
    'TokenBearer',
    'get_write_offs_repository',
    'get_external_database_service',
)


class TokenBearer(HTTPBearer):

    def __init__(self, ):
        super().__init__(scheme_name='Token', description='Token')

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        return credentials.credentials


def get_write_offs_repository() -> WriteOffRepository:
    return WriteOffRepository(sessionmaker(engine))


def get_external_database_service() -> ExternalDatabaseService:
    return ExternalDatabaseService(base_url=settings.external_database_api_url)
