import datetime

import pytest

import models
from services.parsers import is_passed_periodic_time, determine_event_type_or_none


@pytest.mark.parametrize(
    'passed_seconds,interval_in_seconds,deviation,expected',
    [
        (0, 60, 10, True),
        (100, 60, 10, False),
        (106, 60, 5, False),
        (94, 60, 5, False),
        (130, 150, 20, True),
        (129, 150, 20, False),
        (171, 150, 20, False),
    ]
)
def test_is_ingredient_expired_correct_cases(passed_seconds, interval_in_seconds, deviation, expected):
    assert is_passed_periodic_time(passed_seconds, interval_in_seconds, deviation) == expected


def test_is_ingredient_expired_negative_passed_seconds():
    with pytest.raises(ValueError) as error:
        is_passed_periodic_time(-1, interval_in_seconds=10, deviation_in_seconds=10)
    assert error.value.args[0] == 'Passed time can not be negative'


def test_is_ingredient_expired_deviation_bigger_than_interval():
    with pytest.raises(ValueError) as error:
        is_passed_periodic_time(0, interval_in_seconds=10, deviation_in_seconds=11)
    assert error.value.args[0] == 'Deviation can not be bigger than interval'


@pytest.fixture(scope='function')
def patch_get_moscow_datetime_now():
    def fake_get_moscow_datetime_now():
        return datetime.datetime(year=2022, month=8, day=10, hour=15, minute=10, second=20)

    from resources import time_helpers
    time_helpers.get_moscow_datetime_now = fake_get_moscow_datetime_now


@pytest.mark.parametrize(
    'time_as_string,event_type',
    [
        ('15:00', models.EventType.ALREADY_EXPIRED),
        ('14:50', models.EventType.ALREADY_EXPIRED),
        ('14:40', models.EventType.ALREADY_EXPIRED),
        ('14:30', models.EventType.ALREADY_EXPIRED),
        ('12:20', models.EventType.ALREADY_EXPIRED),
        ('05:10', models.EventType.ALREADY_EXPIRED),
        ('15:20:40', models.EventType.EXPIRE_AT_10_MINUTES),
        ('15:25:00', models.EventType.EXPIRE_AT_15_MINUTES),
        ('15:15:00', models.EventType.EXPIRE_AT_5_MINUTES),
        ('15:16', None),
        ('12:17', None),
        ('18:45', None),
        ('23:02', None),
    ]
)
def test_determine_event_types(time_as_string, event_type, patch_get_moscow_datetime_now):
    write_off = models.NotWrittenOffIngredient(ingredient_name='Тесто 35', write_off_at=time_as_string)
    assert determine_event_type_or_none(write_off) == event_type
