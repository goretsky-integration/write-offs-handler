from loguru import logger

from settings import LOGS_FILE_PATH, get_app_settings

__all__ = (
    'logger',
)

level = 'DEBUG' if get_app_settings().debug else 'INFO'

logger.add(LOGS_FILE_PATH, level=level)
