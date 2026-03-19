# models/lstm/features.py

"""
⚠️ IMPORTANT
This feature order MUST match training exactly.
Changing this file REQUIRES retraining the LSTM.
"""

LOG_LEVEL_MAP = {
    "INFO": 0,
    "WARN": 1,
    "ERROR": 2,
}

SERVICE_MAP = {
    "AuthService": 0,
    "PaymentService": 1,
    "OrderService": 2,
}

def extract_features(parsed_log):
    """
    Returns EXACTLY 5 features (same as training)
    Order matters.
    """

    hour = parsed_log["timestamp"].hour

    log_level = LOG_LEVEL_MAP.get(parsed_log["level"], 0)
    service = SERVICE_MAP.get(parsed_log["service"], 0)

    message_length = len(parsed_log["message"])
    is_error = 1 if parsed_log["level"] == "ERROR" else 0

    return [
        hour,
        log_level,
        service,
        message_length,
        is_error
    ]
