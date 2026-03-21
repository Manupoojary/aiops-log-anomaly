# 🔍 LogIQ — AIOps Log Anomaly Detection Platform

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-IsolationForest-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache-Kafka-231F20?style=flat&logo=apachekafka&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elastic-Search-005571?style=flat&logo=elasticsearch&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)

**🌐 Live Demo → [https://aiops-log-anomaly-qrnsm8xw9wykuppcv3vtwd.streamlit.app](https://aiops-log-anomaly-qrnsm8xw9wykuppcv3vtwd.streamlit.app)**

> ⚠️ Note: App may take ~30 seconds to wake up if it has been inactive.

---

## What is this?

Large-scale systems generate thousands of log lines per minute across multiple services.
Manually identifying anomalies is slow, error-prone, and doesn't scale.

**LogIQ** automates this using unsupervised ML — detecting abnormal patterns in real time
without requiring any labelled training data. It watches a live log stream, scores each
entry using Isolation Forest or LSTM, and surfaces anomalies on an interactive dashboard.

This project has two versions:

| Version | Description |
|---|---|
| **Full pipeline** | Kafka + Elasticsearch + Grafana + Docker (industry-grade) |
| **Live demo** | Streamlit + SQLite + file watcher (deployable, portfolio-ready) |

---

## Dashboard Preview

> **Live metrics from the deployed app:**
> - **1,653** total logs processed
> - **154** anomalies detected (9.32% anomaly rate)
> - Services monitored: AuthService · OrderService · PaymentService
> - Real-time log feed with per-row anomaly scoring
> - Switch between Isolation Forest and LSTM from the sidebar

*Screenshots:*

![Dashboard Overview](screenshots/dashboard_overview.png)
*Main dashboard — live metrics, algorithm selector, start/stop controls*

![Charts](screenshots/charts.png)
*Log volume by service (bar chart) + anomaly vs normal breakdown (pie chart)*

![Timeline](screenshots/timeline.png)
*Live anomaly timeline — total logs vs anomalies over time*

![Log Feed](screenshots/log_feed.png)
*Live log feed — timestamp, level, service, message, anomaly flag per row*

---

## Features

- **Real-time log monitoring** — watches a live log file and detects new entries every second using a file watcher (similar to how Filebeat works in production ELK stacks)
- **Dual ML models** — switch between Isolation Forest (fast, unsupervised) and LSTM (sequential pattern learning) from the sidebar at any time
- **Per-service breakdown** — log volume and anomaly rates split by service (AuthService, OrderService, PaymentService)
- **Live anomaly timeline** — plots total log volume vs anomalies detected over time
- **Live log feed** — scrollable table showing each log entry with its anomaly score
- **Zero labelled data required** — Isolation Forest trains on the first 50 logs unsupervised
- **Full production pipeline** — Kafka + Elasticsearch + Grafana via Docker Compose for industry-grade deployment

---

## How It Works

```
Live log file (live_logs.log)
        │
        ▼
  File Watcher
(detects new lines)
        │
        ▼
Feature Extraction
(log level, message length, user_id → numerical features)
        │
        ▼
   ┌────┴────┐
   │         │
Isolation   LSTM
Forest    (sequence
(outlier   anomaly)
 score)
   │         │
   └────┬────┘
        │
   Anomaly Score
(0 = Normal, 1 = Anomaly)
        │
        ▼
   SQLite Storage
        │
        ▼
Streamlit Dashboard
(metrics · charts · live feed)
```

---

## Full Production Architecture (Docker)

```
Applications / Servers
        │ (logs)
        ▼
   Filebeat / Fluentd
        │
        ▼
      Kafka ──────────────────┐
        │                     │
        ▼                     │
  Log Processing              │
(Parsing + Feature Engg)      │
        │                     │
        ▼                     │
ML Anomaly Engine             │
(Isolation Forest / LSTM)     │
        │                     │
        ▼                     │
 Elasticsearch ←──────────────┘
        │
        ▼
  Grafana / Kibana Dashboard
        │
        ▼
 Alerting (Email / Slack)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Models | scikit-learn (Isolation Forest), TensorFlow/Keras (LSTM) |
| Feature Engineering | NumPy, Pandas |
| Log Streaming | Apache Kafka |
| Storage (prod) | Elasticsearch |
| Storage (demo) | SQLite |
| Visualization (prod) | Grafana, Kibana |
| Visualization (demo) | Streamlit, Plotly |
| Log Ingestion | Filebeat, Kafka Producer |
| Backend API | Flask |
| Frontend (prod) | HTML / CSS / JS |
| Orchestration | Docker Compose |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
aiops-log-anomaly/
│
├── streamlit_demo/             # Live deployable demo
│   ├── app.py                  # Streamlit dashboard (main entry point)
│   ├── log_generator.py        # Generates live logs every second
│   ├── file_watcher.py         # Watches log file for new entries
│   ├── detector.py             # Isolation Forest + LSTM detection
│   ├── database.py             # SQLite storage layer
│   └── requirements.txt        # Lightweight dependencies
│
├── ingestion/                  # Full pipeline — Kafka producer
│   └── kafka_producer.py
│
├── processing/                 # Full pipeline — consumer + ML
│   ├── pipeline.py
│   ├── log_parser.py
│   └── feature_engineering.py
│
├── models/                     # ML models
│   ├── isolation_forest.py
│   └── lstm_model.py
│
├── storage/                    # Elasticsearch writer
│   └── elastic_writer.py
│
├── backend/                    # Flask REST API
│   └── app.py
│
├── frontend/                   # HTML/CSS/JS dashboard
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/                       # Log datasets
│   └── generate_logs.py
│
├── docker-compose.yml          # Kafka + Elasticsearch + Grafana
├── requirements.txt            # Full dependencies
└── README.md
```

---

## Run Locally (Live Demo)

```bash
# 1. Clone the repo
git clone https://github.com/Manupoojary/aiops-log-anomaly
cd aiops-log-anomaly/streamlit_demo

# 2. Create virtual environment
conda create -n aiops python=3.10
conda activate aiops

# 3. Install dependencies
pip install -r requirements.txt

# 4. Terminal 1 — Start the log generator
python log_generator.py

# 5. Terminal 2 — Launch the Streamlit dashboard
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501), click **Start Watching**, and watch anomalies get detected live.

---

## Run Full Production Pipeline (Docker)

```bash
# 1. Start all services
docker compose up -d

# 2. Generate synthetic logs
python data/generate_logs.py

# 3. Start Kafka producer
python ingestion/kafka_producer.py

# 4. Start ML pipeline
python -m processing.pipeline

# 5. Open Elasticsearch
# http://localhost:9200/logs-aiops/_count

# 6. Open Grafana dashboard
# http://localhost:3000 (admin / admin)
```

---

## Sample Log Format

```
2026-03-21 12:06:44 INFO  PaymentService  Payment completed       user_id=203
2026-03-21 12:06:45 INFO  AuthService     User authenticated      user_id=87
2026-03-21 12:06:46 ERROR AuthService     Invalid token           user_id=412  ← anomaly
2026-03-21 12:06:47 WARN  OrderService    Timeout occurred        user_id=56   ← anomaly
2026-03-21 12:06:48 INFO  OrderService    Order created           user_id=301
```

---

## ML Approach

### Isolation Forest (default)
- Unsupervised — no labelled anomaly data needed
- Trains on the first 50 log entries to learn normal behaviour
- Scores each new log — outliers get flagged as anomalies
- Fast, lightweight, industry-standard baseline
- Used by Netflix, Google, Amazon for log anomaly detection

### LSTM
- Learns sequential patterns across log entries
- Better at catching anomalies that depend on context (e.g. a burst of ERRORs after a long sequence of INFOs)
- Detects temporal anomalies that Isolation Forest misses
- Requires more logs to warm up but catches subtle pattern breaks

> *"This system mirrors real AIOps pipelines used at Netflix and Google — combining unsupervised ML with real-time log streaming and live observability dashboards."*

---

## Interview Highlights

- Designed an end-to-end AIOps platform for detecting anomalies in large-scale system logs using Isolation Forest and LSTM models
- Built a real-time log ingestion pipeline using Kafka and Elasticsearch with Grafana dashboards for SRE monitoring
- Implemented a file watcher that tails live log files every second — similar to how Filebeat works in production ELK stacks
- Deployed a fully functional live demo on Streamlit Cloud with algorithm switching, live metrics, and anomaly timeline

---

## What I Learned

- How to convert raw unstructured log text into ML-ready numerical features
- The practical tradeoffs between Isolation Forest (speed) and LSTM (context awareness) for streaming anomaly detection
- Building a real-time data pipeline from log file → feature extraction → model inference → live UI
- How Kafka, Elasticsearch, and Grafana work together in a production AIOps system
- Deploying a Streamlit ML app to production with background threading for continuous log generation

---

## Author

**Manohara Poojary** — AI/ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/manohara-poojary)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github&logoColor=white)](https://github.com/Manupoojary)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:manohar4693@gmail.com)

