from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'Settings',
    'settings',
)

load_dotenv()


class Settings(BaseSettings):
    host: str = Field(env='APP_HOST')
    port: int = Field(env='APP_PORT')
    debug: bool = Field(env='DEBUG')
    token: str = Field(env='TOKEN')
    rabbitmq_url: str = Field(env='RABBITMQ_URL')


settings = Settings()
