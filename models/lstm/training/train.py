import numpy as np
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

# ---------------- CONFIG ----------------
DATA_PATH = "models/lstm/training/X_train.npy"
MODEL_PATH = "models/lstm/artifacts/lstm_model.h5"
THRESHOLD_PATH = "models/lstm/artifacts/threshold.json"

EPOCHS = 20
BATCH_SIZE = 32
PERCENTILE = 95  # anomaly threshold


# ---------------- LOAD DATA ----------------
print("Loading dataset...")
X = np.load(DATA_PATH)

# Predict next step: use first 9 to predict 10th
X_input = X[:, :-1, :]   # (samples, 9, features)
y_target = X[:, -1, :]   # (samples, features)

print(f"Training data shape: {X_input.shape}")
print(f"Target shape: {y_target.shape}")


# ---------------- MODEL ----------------
model = Sequential([
    LSTM(64, input_shape=(X_input.shape[1], X_input.shape[2])),
    Dense(y_target.shape[1])
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

print("Training LSTM model...")
model.fit(
    X_input,
    y_target,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1,
    verbose=1
)


# ---------------- THRESHOLD ----------------
print("Calculating anomaly threshold...")
predictions = model.predict(X_input)
errors = np.mean((predictions - y_target) ** 2, axis=1)

threshold = float(np.percentile(errors, PERCENTILE))

print(f"Anomaly threshold set to: {threshold}")


# ---------------- SAVE ----------------
model.save(MODEL_PATH)
with open(THRESHOLD_PATH, "w") as f:
    json.dump({"threshold": threshold}, f)

print("Model and threshold saved ✅")
