# storage/elastic_writer.py
from elasticsearch import Elasticsearch

ES_INDEX = "logs-aiops"

def get_es():
    return Elasticsearch("http://localhost:9200")

def write_log(es, parsed, anomaly):
    doc = {
        "timestamp": parsed["timestamp"].isoformat(),
        "service": parsed["service"],
        "level": parsed["level"],
        "message": parsed["message"],
        "user_id": parsed["user_id"],
        "anomaly": bool(anomaly)
    }
    es.index(index=ES_INDEX, document=doc)
