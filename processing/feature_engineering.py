# processing/feature_engineering.py

def extract_features(parsed_log):
    """
    Returns a numeric feature vector.
    MUST match training features exactly.
    """

    level_map = {
        "INFO": 0,
        "WARN": 1,
        "ERROR": 2
    }

    level = level_map.get(parsed_log["level"], 0)
    message_len = len(parsed_log["message"])
    user_id = int(parsed_log["user_id"])

    # timestamp is string → extract hour safely
    ts = parsed_log["timestamp"]
    hour = int(ts[11:13]) if isinstance(ts, str) else ts.hour

    is_error = 1 if parsed_log["level"] == "ERROR" else 0

    return [
        level,
        message_len,
        user_id,
        hour,
        is_error
    ]
