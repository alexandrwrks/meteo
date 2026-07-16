from datetime import datetime, timedelta, time


def round_to_hour(value: time) -> datetime:
    dt = datetime.combine(datetime.today(), value)

    if dt.minute >= 30:
        dt += timedelta(hours=1)

    return dt.replace(
        minute=0,
        second=0,
        microsecond=0,
    )

def floor_to_hour(value: time) -> datetime:
    return datetime.combine(
        datetime.today(),
        value.replace(minute=0, second=0, microsecond=0),
    )