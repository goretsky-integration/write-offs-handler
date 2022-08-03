from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'get_app_settings',
    'init_settings',
)


class AppSettings(BaseSettings):
    host: str = Field(env='APP_HOST')
    port: int = Field(env='APP_PORT')
    debug: bool = Field(env='DEBUG')


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


def init_settings():
    load_dotenv()
    get_app_settings()
