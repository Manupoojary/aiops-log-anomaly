import re
import os
import time

LOG_FILE = "../data/live_logs.log"

LOG_PATTERN = re.compile(
    r"(.*?) (INFO|WARN|ERROR) (\w+) (.*?) user_id=(\d+)"
)

def parse_line(line):
    match = LOG_PATTERN.match(line.strip())
    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2),
            "service": match.group(3),
            "message": match.group(4),
            "user_id": int(match.group(5))
        }
    return None

def get_new_logs(last_position=0):
    new_logs = []
    new_position = last_position

    if not os.path.exists(LOG_FILE):
        return [], last_position

    with open(LOG_FILE, "r") as f:
        f.seek(last_position)
        for line in f:
            parsed = parse_line(line)
            if parsed:
                new_logs.append(parsed)
        new_position = f.tell()

    return new_logs, new_position