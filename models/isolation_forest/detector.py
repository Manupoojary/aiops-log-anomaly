import numpy as np
from sklearn.ensemble import IsolationForest


class IsolationForestDetector:
    def __init__(self):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=42
        )
        self.is_trained = False

    def fit(self, X):
        X = np.asarray(X, dtype=np.float32)
        self.model.fit(X)
        self.is_trained = True

    def predict(self, X):
        X = np.asarray(X, dtype=np.float32)

        if not self.is_trained:
            return False

        pred = self.model.predict(X.reshape(1, -1))[0]
        return pred == -1
