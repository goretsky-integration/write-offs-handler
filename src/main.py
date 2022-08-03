import uvicorn

from app import app
from settings import get_app_settings, init_settings


def main():
    init_settings()
    app_settings = get_app_settings()
    uvicorn.run(
        'app:app',
        host=app_settings.host,
        port=app_settings.port,
        debug=app_settings.debug,
        reload=app_settings.debug,
    )


if __name__ == '__main__':
    main()
