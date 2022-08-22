from datetime import datetime, timedelta

__all__ = (
    'get_moscow_datetime_now',
)


def get_moscow_datetime_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)
