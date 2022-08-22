import datetime

__all__ = (
    'get_moscow_datetime_now',
)


def get_moscow_datetime_now() -> datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)
