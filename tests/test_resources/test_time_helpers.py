from resources.time_helpers import get_moscow_datetime_now, datetime


def test_get_moscow_datetime_now(fake_datetime):
    real_datetime = datetime.datetime
    datetime.datetime = fake_datetime

    assert get_moscow_datetime_now() == (fake_datetime.utcnow() + datetime.timedelta(hours=3))

    datetime.datetime = real_datetime
