import numpy as np

LEVEL_MAP = {
    "INFO": 0,
    "WARN": 1,
    "ERROR": 2
}

def extract_features(parsed_log: dict) -> np.ndarray:
    """
    Feature vector:
    [level, message_length, user_id]
    """

    level = LEVEL_MAP.get(parsed_log["level"], 0)
    message_length = len(parsed_log["message"])
    user_id = parsed_log.get("user_id", 0)

    return np.array([level, message_length, user_id], dtype=float)
