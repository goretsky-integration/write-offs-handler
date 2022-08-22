from sse_starlette import ServerSentEvent

from resources.events import get_ping_message, datetime


def test_ping_message_factory():
    time = datetime.datetime(2022, 2, 2, 3, 4, 1)

    class FakeDatetime:

        @classmethod
        def utcnow(cls):
            return time

    datetime.datetime = FakeDatetime
    ping_message_response = get_ping_message()
    expected_ping_message = ServerSentEvent(data={'time': time}, event='ping')
    assert expected_ping_message.data == ping_message_response.data
    assert expected_ping_message.event == ping_message_response.event
