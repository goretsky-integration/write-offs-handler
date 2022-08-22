from sse_starlette import ServerSentEvent

from resources.events import get_ping_message, datetime


def test_ping_message_factory(fake_datetime):
    real_datetime = datetime.datetime
    datetime.datetime = fake_datetime

    ping_message_response = get_ping_message()
    expected_ping_message = ServerSentEvent(data={'time': fake_datetime.time}, event='ping')

    assert expected_ping_message.data == ping_message_response.data
    assert expected_ping_message.event == ping_message_response.event

    datetime.datetime = real_datetime
