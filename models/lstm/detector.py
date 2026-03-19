import json
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque
from .config import SEQUENCE_LENGTH, MODEL_PATH, THRESHOLD_PATH


class LSTMDetector:
    def __init__(self):
        print("Loading LSTM model...")
        self.model = load_model(MODEL_PATH, compile=False)

        print("Loading anomaly threshold...")
        with open(THRESHOLD_PATH, "r") as f:
            self.threshold = float(json.load(f)["threshold"])

        self.sequence = deque(maxlen=SEQUENCE_LENGTH)
        self.feature_dim = self.model.input_shape[-1]

        print("LSTM model loaded successfully")
        print(f"Sequence length: {SEQUENCE_LENGTH}")
        print(f"Feature dimension: {self.feature_dim}")
        print(f"Anomaly threshold: {self.threshold}")

    def predict(self, feature_vector):
        feature_vector = np.asarray(feature_vector, dtype=np.float32)

        if feature_vector.shape[0] != self.feature_dim:
            raise ValueError(
                f"LSTM feature mismatch: expected {self.feature_dim}, "
                f"got {feature_vector.shape[0]}"
            )

        self.sequence.append(feature_vector)

        if len(self.sequence) < SEQUENCE_LENGTH:
            return False  # warm-up

        seq_array = np.array(self.sequence).reshape(
            1, SEQUENCE_LENGTH, self.feature_dim
        )

        reconstruction = self.model.predict(seq_array, verbose=0)
        mse = np.mean((seq_array - reconstruction) ** 2)

        return mse > self.threshold
