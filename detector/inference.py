"""
inference.py — YOLO inference on chart screenshots.

Runs detection on a single image and returns a structured result.
"""

from pathlib import Path

import numpy as np

from detector.model import load_model
from detector.postprocess import select_rightmost_box, filter_by_confidence, box_to_dict
from configs.settings import CONFIDENCE_THRESHOLD


def run_inference(image: str | Path | np.ndarray, ticker: str, timeframe: str = "1D") -> dict:
    """Run YOLO inference on a single chart screenshot."""

    model = load_model()

    # Run YOLO inference — accepts both file paths and numpy arrays
    if isinstance(image, np.ndarray):
        results = model(image, conf=CONFIDENCE_THRESHOLD)
    else:
        results = model(str(image), conf=CONFIDENCE_THRESHOLD)

    if not results or len(results[0].boxes) == 0:
        return {
            "ticker": ticker,
            "timeframe": timeframe,
            "label": None,
            "confidence": None,
            "box": None,
            "detected": False,
            "all_count": 0,
            "is_recent": False,
        }

    all_boxes = results[0].boxes
    total_count = len(all_boxes)

    # Filter by confidence
    good_boxes = filter_by_confidence(all_boxes, CONFIDENCE_THRESHOLD)

    if not good_boxes:
        return {
            "ticker": ticker,
            "timeframe": timeframe,
            "label": None,
            "confidence": None,
            "box": None,
            "detected": False,
            "all_count": total_count,
            "is_recent": False,
        }

    # Select the rightmost (most recent) box
    best_box = select_rightmost_box(good_boxes)

    # Convert to dictionary
    result = box_to_dict(best_box, model.names, ticker, timeframe)
    result["detected"] = True
    result["all_count"] = total_count

    return result
