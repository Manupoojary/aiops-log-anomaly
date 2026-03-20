import random
import time
from datetime import datetime
import os

SERVICES = ["AuthService", "PaymentService", "OrderService"]

NORMAL_MSGS = [
    "Request processed successfully",
    "User authenticated",
    "Order created",
    "Payment completed",
    "Session started",
    "Cache hit",
    "Health check passed"
]

ERROR_MSGS = [
    "Invalid token",
    "Database connection failed",
    "Timeout occurred",
    "Null pointer exception",
    "Memory overflow",
    "Service unavailable"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "data", "live_logs.log")

def generate_log_line():
    is_anomaly = random.random() < 0.05
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = "ERROR" if is_anomaly else random.choice(["INFO", "INFO", "INFO", "WARN"])
    service = random.choice(SERVICES)
    message = random.choice(ERROR_MSGS) if is_anomaly else random.choice(NORMAL_MSGS)
    user_id = random.randint(1, 500)
    return f"{timestamp} {level} {service} {message} user_id={user_id}\n"


def start_generating():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    print(f"Starting log generation → {LOG_FILE}")
    with open(LOG_FILE, "a") as f:
        while True:
            line = generate_log_line()
            f.write(line)
            f.flush()  # Important! writes immediately to file
            print(f"Written: {line.strip()}")
            time.sleep(1)

if __name__ == "__main__":
    start_generating()