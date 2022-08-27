import uvicorn

from fastapi import FastAPI

import api
from settings import get_app_settings


def get_application() -> FastAPI:
    app_settings = get_app_settings()
    application = FastAPI(
        debug=app_settings.debug,
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.debug,
    )
    application.include_router(api.events.router)
    application.include_router(api.spreadsheets.router)
    return application


def main():
    uvicorn.run('main:app')


app = get_application()

if __name__ == '__main__':
    main()
