import datetime

from sse_starlette import ServerSentEvent

__all__ = (
    'get_ping_message',
)


def get_ping_message() -> ServerSentEvent:
    return ServerSentEvent(
        event='ping',
        data={
            'time': datetime.datetime.utcnow().isoformat(),
        },
    )
