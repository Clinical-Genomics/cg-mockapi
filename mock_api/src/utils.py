# mock_api/src/utils.py
from datetime import datetime
from zoneinfo import ZoneInfo


def current_time_se() -> datetime:
    """Get the current time in Sweden's time zone as a timezone-aware datetime."""
    sweden_tz = ZoneInfo("Europe/Stockholm")
    return datetime.now(sweden_tz)
