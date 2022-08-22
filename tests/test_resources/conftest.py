import datetime

import pytest


@pytest.fixture
def fake_datetime():
    class FakeDatetime:
        time = datetime.datetime(2022, 2, 2, 3, 4, 1)

        @classmethod
        def utcnow(cls):
            return cls.time

    return FakeDatetime
