import uvicorn
from fastapi import FastAPI
from loguru import logger

import api
from settings import get_app_settings, logging_settings


def on_startup():
    logger.add(logging_settings.logfile_path, level=logging_settings.level)


def get_application() -> FastAPI:
    app_settings = get_app_settings()
    application = FastAPI(
        title='Write Offs API',
        debug=app_settings.debug,
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.debug,
    )
    application.include_router(api.router)
    return application


def main():
    uvicorn.run('main:app')


app = get_application()

if __name__ == '__main__':
    main()
