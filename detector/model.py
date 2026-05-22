"""
model.py — YOLO model loading.

Loads the trained YOLOv8 model ONCE and exposes a reusable model object.
Avoids reloading the model for every image.
"""

from ultralytics import YOLO
from configs.settings import MODEL_PATH


# --------------------------------------------------------------------------
# Module-level model cache — loaded once, reused everywhere
# --------------------------------------------------------------------------

_model = None


def load_model() -> YOLO:
    """
    Load the YOLO model from disk (or return the cached instance).

    The model is loaded once on first call and cached for subsequent calls.
    This avoids the expensive model load for every image.

    Returns:
        The loaded YOLO model instance.
    """

    global _model

    if _model is not None:
        return _model

    print(f"[model] Loading YOLO model from: {MODEL_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}\n"
            "Make sure stockmarket-pattern-detection-yolov8/model.pt exists."
        )

    _model = YOLO(str(MODEL_PATH))

    # Print available class names for reference
    print(f"[model] Classes: {_model.names}")
    print("[model] Model loaded successfully.")

    return _model
