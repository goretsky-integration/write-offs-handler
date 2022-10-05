from sqlalchemy.orm import sessionmaker

__all__ = (
    'BaseRepository',
)


class BaseRepository:

    def __init__(self, session_maker: sessionmaker):
        self._session_maker = session_maker
