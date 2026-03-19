# data/generate_logs.py
import random
from datetime import datetime, timedelta

services = ["AuthService", "PaymentService", "OrderService"]
levels = ["INFO", "WARN", "ERROR"]

normal_msgs = [
    "Request processed successfully",
    "User authenticated",
    "Order created",
    "Payment completed"
]

error_msgs = [
    "Invalid token",
    "Database connection failed",
    "Timeout occurred",
    "Null pointer exception"
]

start_time = datetime.now()

with open("synthetic_logs.log", "w") as f:
    for i in range(5000):
        timestamp = start_time + timedelta(seconds=i)
        service = random.choice(services)

        if random.random() < 0.95:
            level = "INFO"
            msg = random.choice(normal_msgs)
        else:
            level = "ERROR"
            msg = random.choice(error_msgs)

        log = f"{timestamp} {level} {service} {msg} user_id={random.randint(1,500)}\n"
        f.write(log)
