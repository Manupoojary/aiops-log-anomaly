# Automated Log Anomaly Detection (AIOps)

An industry-level AIOps platform for detecting anomalies in large-scale system logs.

## Tech Stack
Python | Kafka | Elasticsearch | Grafana | Docker | Scikit-learn | TensorFlow

## Features
- Real-time log ingestion via Kafka
- Log parsing and feature engineering
- Anomaly detection using Isolation Forest and LSTM
- Elasticsearch storage
- Grafana visualization dashboard
- Flask backend with HTML frontend

## How to Run
```bash
# Step 1 - Start Docker services
docker compose up -d

# Step 2 - Generate synthetic logs
python data/generate_logs.py

# Step 3 - Start Kafka producer
python ingestion/kafka_producer.py

# Step 4 - Start pipeline
python -m processing.pipeline
```

## Architecture
Browser → Flask Backend → Pipeline → Kafka → ML Model → Elasticsearch → Grafana/Dashboard

## Live Demo
🌐 [Live App](https://aiops-log-anomaly-qrnsm8xw9wykuppcv3vtwd.streamlit.app)

AIOps Log Anomaly Detection
🌐 Live: https://aiops-log-anomaly-qrnsm8xw9wykuppcv3vtwd.streamlit.app
🔗 GitHub: github.com/Manupoojary/aiops-log-anomaly

