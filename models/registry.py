# models/registry.py

from models.isolation_forest.detector import IsolationForestDetector
from models.lstm.detector import LSTMDetector

# Central model registry
MODEL_REGISTRY = {
    "isolation_forest": IsolationForestDetector,
    "lstm": LSTMDetector,
}

def get_model(name: str):
    """
    Return an initialized detector by name
    """
    name = name.lower()

    if name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {name}")

    return MODEL_REGISTRY[name]()

def list_models():
    """
    Return available model names (for UI)
    """
    return list(MODEL_REGISTRY.keys())
