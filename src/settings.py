import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'get_app_settings',
    'get_redis_settings',
    'get_database_settings',
    'get_rabbitmq_settings',
    'ROOT_PATH',
    'LOGS_FILE_PATH',
)

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOGS_FILE_PATH = ROOT_PATH / 'logs.log'

load_dotenv()


class AppSettings(BaseSettings):
    host: str = Field(env='APP_HOST')
    port: int = Field(env='APP_PORT')
    debug: bool = Field(env='DEBUG')


class RedisSettings(BaseSettings):
    url: str = Field(env='REDIS_URL')


class RabbitMQSettings(BaseSettings):
    url: str = Field(env='RABBITMQ_URL')


class DatabaseSettings(BaseSettings):
    host: str = Field(env='DATABASE_HOST')
    port: str = Field(env='DATABASE_PORT')
    name: str = Field(env='DATABASE_NAME')
    user: str = Field(env='DATABASE_USER')
    password: str = Field(env='DATABASE_PASSWORD')

    @property
    def url(self) -> str:
        return f'{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_redis_settings() -> RedisSettings:
    return RedisSettings()


@lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
