# processing/pipeline.py
print("PIPELINE FILE LOADED")

import json
from kafka import KafkaConsumer


from processing.parsing.log_parser import parse_log
from processing.feature_engineering import extract_features
from models.registry import get_model
from storage.elastic_writer import get_es, write_log

KAFKA_TOPIC = "logs-topic"
KAFKA_BOOTSTRAP = "localhost:9092"

def run_pipeline(model_name):
    print(f"\nRunning pipeline using: {model_name.upper()}")
    print("Pipeline started, waiting for logs...\n")

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="latest",
        value_deserializer=lambda x: json.loads(x.decode())
    )

    detector = get_model(model_name)
    es = get_es()

    train_buffer = []

    for msg in consumer:
        raw = msg.value
        print("RAW MESSAGE:", raw)

        parsed = parse_log(raw)
        if not parsed:
            print("Unmatched log")
            continue

        features = extract_features(parsed)

        # Isolation Forest
        if model_name == "isolation_forest":
            train_buffer.append(features)
            if not detector.is_trained and len(train_buffer) >= 50:
                detector.fit(train_buffer)
            anomaly = detector.predict(features)

        # LSTM
        else:
            anomaly = detector.predict(features)

        write_log(es, parsed, anomaly)
        print(f"Stored log | Anomaly: {anomaly}")

if __name__ == "__main__":
    import sys
    model = sys.argv[1] if len(sys.argv) > 1 else "isolation_forest"
    run_pipeline(model)
