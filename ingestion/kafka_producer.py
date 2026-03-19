from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

with open("data/synthetic_logs.log") as f:
    for line in f:
        producer.send("logs-topic", {"log": line})
        time.sleep(0.01)
