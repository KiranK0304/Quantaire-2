"""
inference.py — YOLO inference on chart screenshots.

Runs detection on a single image and returns a structured result.
Selects only the rightmost/latest box (most recent pattern on the chart).
"""

from pathlib import Path

import numpy as np

from detector.model import load_model
from detector.postprocess import select_rightmost_box, filter_by_confidence, box_to_dict
from configs.settings import CONFIDENCE_THRESHOLD


def run_inference(image: str | Path | np.ndarray, ticker: str) -> dict:
    """
    Run YOLO inference on a single chart screenshot.

    Steps:
      1. Load the model (cached after first call)
      2. Run inference with confidence threshold
      3. Filter low-confidence detections
      4. Select the rightmost/latest box
      5. Return structured detection result

    Args:
        image:  Path to the chart screenshot PNG, OR a numpy array (BGR).
        ticker: Stock ticker name (e.g. "RELIANCE").

    Returns:
        Detection dict with keys:
          - ticker:     str
          - label:      str (pattern name) or None
          - confidence: float or None
          - box:        [x1, y1, x2, y2] or None
          - detected:   bool
          - all_count:  int (total detections before filtering)
    """

    model = load_model()

    # Run YOLO inference — accepts both file paths and numpy arrays
    if isinstance(image, np.ndarray):
        results = model(image, conf=CONFIDENCE_THRESHOLD)
    else:
        results = model(str(image), conf=CONFIDENCE_THRESHOLD)

    # Check if any detections exist
    if not results or len(results[0].boxes) == 0:
        return {
            "ticker": ticker,
            "label": None,
            "confidence": None,
            "box": None,
            "detected": False,
            "all_count": 0,
        }

    all_boxes = results[0].boxes
    total_count = len(all_boxes)

    # Filter by confidence
    good_boxes = filter_by_confidence(all_boxes, CONFIDENCE_THRESHOLD)

    if not good_boxes:
        return {
            "ticker": ticker,
            "label": None,
            "confidence": None,
            "box": None,
            "detected": False,
            "all_count": total_count,
        }

    # Select the rightmost (most recent) box
    best_box = select_rightmost_box(good_boxes)

    # Convert to dictionary
    result = box_to_dict(best_box, model.names, ticker)
    result["detected"] = True
    result["all_count"] = total_count

    return result
