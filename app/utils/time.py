from datetime import datetime, timedelta, timezone

def get_vietnam_time():
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
