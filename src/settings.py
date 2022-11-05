from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'get_app_settings',
    'get_rabbitmq_settings',
)

load_dotenv()


class AppSettings(BaseSettings):
    host: str = Field(env='APP_HOST')
    port: int = Field(env='APP_PORT')
    debug: bool = Field(env='DEBUG')


class RabbitMQSettings(BaseSettings):
    url: str = Field(env='RABBITMQ_URL')


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
