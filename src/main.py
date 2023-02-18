import uvicorn
from fastapi import FastAPI

import api.routers
from settings import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title='Write Offs API',
        debug=settings.debug,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
    application.include_router(api.routers.write_offs.router)
    return application


def main():
    uvicorn.run('main:app')


app = get_application()

if __name__ == '__main__':
    main()
