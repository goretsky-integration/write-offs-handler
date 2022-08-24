import models
from resources import time_helpers


def is_passed_periodic_time(
        passed_seconds: int | float,
        interval_in_seconds: int,
        deviation_in_seconds: int,
) -> bool:
    """Determine if precise time (or with deviation) has been passed since 0 seconds.
    It starts counting from 0 to N with some interval.

    Let's define some abbreviations:
        - K: breakpoint after interval.
        - D: deviation from breakpoint.
        - N: number of breakpoint starting since 0.

    0   D            D  K(1) D            D  K(2) D            D  K(3) D            D  K(N)
    |++++------------++++|++++------------++++|++++------------++++|++++------------++++|

    In the picture, the time periods that are correct marked by `+` sign.
    `|` are the breakpoints, so D letters show the beginning and the end of these periods.
    If passed time in these `+` zones, True will be returned.

    The formula is `K(N) = interval * N`.
    If passed seconds equal to `K`,
    or it is between range from `K - deviation` to `K + deviation`,
    True will be returned.

    Examples:
        >>> is_passed_periodic_time(passed_seconds=60, interval_in_seconds=60, deviation_in_seconds=0)
        True
        >>> is_passed_periodic_time(passed_seconds=33, interval_in_seconds=10, deviation_in_seconds=2)
        False
        >>> is_passed_periodic_time(passed_seconds=31, interval_in_seconds=10, deviation_in_seconds=2)
        True

    Args:
        passed_seconds: Passed seconds since 0.
        interval_in_seconds: Values between breakpoints.
        deviation_in_seconds: Deviation from the breakpoints

    Returns:
        True if range (calculated with intervals and deviations) includes passed seconds, otherwise False.
    """
    if passed_seconds < 0:
        raise ValueError('Passed time can not be negative')
    if interval_in_seconds <= deviation_in_seconds:
        raise ValueError('Deviation can not be bigger than interval')

    interval_multiplier = round(passed_seconds / interval_in_seconds)
    comparable_threshold = interval_multiplier * interval_in_seconds
    from_seconds_threshold = comparable_threshold - deviation_in_seconds
    to_seconds_threshold = comparable_threshold + deviation_in_seconds
    return from_seconds_threshold <= passed_seconds <= to_seconds_threshold


def determine_event_type_or_none(write_off: models.NotWrittenOffIngredient) -> models.EventType | None:
    seconds_before_expire = (write_off.write_off_at - time_helpers.get_moscow_datetime_now()).total_seconds()
    if seconds_before_expire <= 0 and is_passed_periodic_time(passed_seconds=abs(seconds_before_expire),
                                                              interval_in_seconds=600,
                                                              deviation_in_seconds=20):
        return models.EventType.ALREADY_EXPIRED
    event_types_by_ranges = (
        (880, 920, models.EventType.EXPIRE_AT_15_MINUTES),
        (580, 620, models.EventType.EXPIRE_AT_10_MINUTES),
        (280, 320, models.EventType.EXPIRE_AT_5_MINUTES),
    )
    for range_start, range_stop, event_type in event_types_by_ranges:
        if range_start <= seconds_before_expire <= range_stop:
            return event_type
