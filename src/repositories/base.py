from sqlalchemy.orm import sessionmaker

__all__ = ('Repository',)


class Repository:

    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
