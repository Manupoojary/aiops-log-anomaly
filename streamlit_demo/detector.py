import numpy as np
from sklearn.ensemble import IsolationForest
import collections

# ── Isolation Forest ──────────────────────────────────────────
if_model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
if_trained = False
if_buffer = []
TRAIN_SIZE = 50

# ── LSTM (lightweight simulation) ─────────────────────────────
lstm_window = collections.deque(maxlen=10)
lstm_trained = False
lstm_baseline = {}

def extract_features(log):
    return [
        len(log['message']),
        1 if log['level'] == 'ERROR' else 0,
        1 if log['level'] == 'WARN' else 0,
        log['user_id']
    ]

def detect_isolation_forest(log):
    global if_trained, if_buffer

    features = extract_features(log)
    if_buffer.append(features)

    if not if_trained and len(if_buffer) >= TRAIN_SIZE:
        if_model.fit(np.array(if_buffer))
        if_trained = True

    if if_trained:
        prediction = if_model.predict([features])[0]
        return 1 if prediction == -1 else 0

    return 1 if log['level'] == 'ERROR' else 0

def detect_lstm(log):
    """
    Lightweight LSTM simulation using sequence pattern baseline.
    Flags a log as anomaly if its pattern deviates from learned sequence.
    """
    global lstm_trained, lstm_baseline

    features = extract_features(log)
    lstm_window.append(features)

    # Build baseline after seeing enough logs
    if not lstm_trained and len(lstm_window) == 10:
        lstm_baseline = {
            "avg_length": np.mean([f[0] for f in lstm_window]),
            "avg_user_id": np.mean([f[3] for f in lstm_window]),
            "error_rate": np.mean([f[1] for f in lstm_window])
        }
        lstm_trained = True

    if lstm_trained:
        # Detect deviation from learned baseline
        msg_len = features[0]
        user_id = features[3]
        is_error = features[1]

        length_deviation = abs(msg_len - lstm_baseline["avg_length"])
        user_deviation = abs(user_id - lstm_baseline["avg_user_id"])
        error_spike = is_error > (lstm_baseline["error_rate"] * 3)

        # Flag as anomaly if strong deviation detected
        if length_deviation > 15 or error_spike or user_deviation > 200:
            return 1

        return 0

    return 1 if log['level'] == 'ERROR' else 0

def detect(log, algorithm="Isolation Forest"):
    if algorithm == "LSTM":
        return detect_lstm(log)
    else:
        return detect_isolation_forest(log)