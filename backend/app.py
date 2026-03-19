from flask import Flask, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
import subprocess
import sys
import os

# ---------------- FIX IMPORT PATH ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.registry import list_models

# ---------------- APP SETUP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ----------------
ES_INDEX = "logs-aiops"
es = Elasticsearch("http://localhost:9200")

pipeline_process = None

# ---------------- STATUS API ----------------
@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "pipeline_running": pipeline_process is not None
    })

# ---------------- METRICS API ----------------
@app.route("/metrics", methods=["GET"])
def metrics():
    try:
        result = es.count(
            index=ES_INDEX,
            query={
                "term": {
                    "anomaly": True
                }
            }
        )

        return jsonify({
            "anomaly_count": result["count"]
        })

    except Exception as e:
        return jsonify({
            "anomaly_count": 0,
            "error": str(e)
        }), 500

# ---------------- START PIPELINE ----------------
@app.route("/start", methods=["POST"])
def start_pipeline():
    global pipeline_process

    if pipeline_process:
        return jsonify({"message": "Pipeline already running"}), 400

    data = request.json or {}
    model = data.get("model", "isolation_forest")

    try:
        pipeline_process = subprocess.Popen(
            [sys.executable, "-m", "processing.pipeline", model],
            cwd=PROJECT_ROOT
        )

        return jsonify({"message": f"Pipeline started with {model}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- STOP PIPELINE ----------------
@app.route("/stop", methods=["POST"])
def stop_pipeline():
    global pipeline_process

    if not pipeline_process:
        return jsonify({"message": "Pipeline not running"}), 400

    pipeline_process.terminate()
    pipeline_process = None

    return jsonify({"message": "Pipeline stopped"}), 200

# ---------------- GET MODELS ----------------
@app.route("/models", methods=["GET"])
def get_models():
    return jsonify(list_models())

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
