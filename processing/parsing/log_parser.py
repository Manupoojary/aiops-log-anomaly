# processing/parsing/log_parser.py
import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r"(?P<timestamp>[\d\-:\. ]+)\s+"
    r"(?P<level>INFO|WARN|ERROR)\s+"
    r"(?P<service>\w+)\s+"
    r"(?P<message>.+?)\s+user_id=(?P<user_id>\d+)"
)

def parse_log(raw):
    """
    Accepts:
    - dict: {"log": "..."}
    - str : "...."
    Returns parsed dict or None
    """
    if isinstance(raw, dict):
        log_line = raw.get("log", "")
    else:
        log_line = str(raw)

    match = LOG_PATTERN.match(log_line.strip())
    if not match:
        return None

    data = match.groupdict()
    data["timestamp"] = datetime.fromisoformat(data["timestamp"])
    data["user_id"] = int(data["user_id"])
    return data
