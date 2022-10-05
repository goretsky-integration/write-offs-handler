from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import get_database_settings

__all__ = (
    'Base',
    'engine',
    'session_maker',
)

engine = create_async_engine(f'postgresql+asyncpg://{get_database_settings().url}', future=True)
Base = declarative_base()
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
