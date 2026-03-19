import numpy as np
from elasticsearch import Elasticsearch
from datetime import datetime

# ---------------- CONFIG ----------------
ES_HOST = "http://localhost:9200"
ES_INDEX = "logs-aiops"

SEQUENCE_LENGTH = 10
OUTPUT_PATH = "models/lstm/training/X_train.npy"

LEVEL_MAP = {
    "INFO": 0,
    "WARN": 1,
    "ERROR": 2
}

SERVICE_MAP = {
    "AuthService": 0,
    "PaymentService": 1,
    "OrderService": 2
}

# ---------------- FEATURE EXTRACTION ----------------
def extract_features(doc):
    """
    Must MATCH runtime feature logic
    """
    level = LEVEL_MAP.get(doc.get("level"), 0)
    service = SERVICE_MAP.get(doc.get("service"), 0)
    user_id = doc.get("user_id", 0)

    ts = doc.get("timestamp")
    if isinstance(ts, str):
        ts = datetime.fromisoformat(ts)

    hour = ts.hour
    message_len = len(doc.get("message", ""))

    return [
        level,
        service,
        user_id,
        hour,
        message_len
    ]

# ---------------- MAIN ----------------
def main():
    print("Connecting to Elasticsearch...")
    es = Elasticsearch(ES_HOST)

    print("Fetching logs from Elasticsearch...")
    resp = es.search(
        index=ES_INDEX,
        size=10000,
        sort="timestamp:asc",
        query={"match_all": {}}
    )

    hits = resp["hits"]["hits"]
    print(f"Fetched {len(hits)} logs")

    if len(hits) < SEQUENCE_LENGTH + 1:
        raise ValueError("Not enough logs to build sequences")

    features = []
    for h in hits:
        features.append(extract_features(h["_source"]))

    features = np.array(features)

    print("Building sequences...")
    X = []
    for i in range(len(features) - SEQUENCE_LENGTH):
        seq = features[i : i + SEQUENCE_LENGTH]
        X.append(seq)

    X = np.array(X)

    print(f"Final dataset shape: {X.shape}")
    print(f"Saving dataset to {OUTPUT_PATH}")
    np.save(OUTPUT_PATH, X)

    print("Dataset build complete ✅")

if __name__ == "__main__":
    main()
