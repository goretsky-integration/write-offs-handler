import pytest

from services.parsers import is_passed_periodic_time


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
        is_passed_periodic_time(-1, interval_in_seconds=10, deviation=10)
    assert error.value.args[0] == 'Passed time can not be negative'


def test_is_ingredient_expired_deviation_bigger_than_interval():
    with pytest.raises(ValueError) as error:
        is_passed_periodic_time(0, interval_in_seconds=10, deviation=11)
    assert error.value.args[0] == 'Deviation can not be bigger than interval'
