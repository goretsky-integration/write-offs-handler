import uvicorn
from fastapi import FastAPI

import api.routers
from api.errors import include_exception_handlers
from database.engine import engine
from database.models import Base
from settings import settings


def on_startup():
    Base.metadata.create_all(engine)


def get_application() -> FastAPI:
    application = FastAPI(
        title='Write Offs API',
        debug=settings.debug,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
    application.include_router(api.routers.write_offs.router)
    application.add_event_handler('startup', on_startup)
    include_exception_handlers(application)
    return application


def main():
    uvicorn.run('main:app')


app = get_application()

if __name__ == '__main__':
    main()
