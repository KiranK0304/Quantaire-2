"""
postprocess.py — Detection post-processing helpers.

Helpers for selecting boxes, filtering confidences, and formatting JSON output.
"""

from configs.settings import RECENCY_THRESHOLD_PERCENT


def select_rightmost_box(boxes):
    """Select the rightmost (latest in time) detection box."""

    if boxes is None or len(boxes) == 0:
        return None

    # x2 (right edge) is at index 2 of xyxy coordinates
    rightmost = max(boxes, key=lambda b: b.xyxy[0][2].item())
    return rightmost


def filter_by_confidence(boxes, min_conf: float = 0.2):
    """Filter detection boxes by minimum confidence threshold."""

    if boxes is None or len(boxes) == 0:
        return []

    return [b for b in boxes if float(b.conf[0]) >= min_conf]


def box_to_dict(box, model_names: dict, ticker: str, timeframe: str = "1D", image_width: int = 1920) -> dict:
    """Convert a single YOLO detection box into a clean dictionary."""
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    label = model_names[cls_id]

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # Check if the right edge of the box is within the recency threshold
    is_recent = x2 >= image_width * (1.0 - RECENCY_THRESHOLD_PERCENT)

    return {
        "ticker": ticker,
        "timeframe": timeframe,
        "label": label,
        "confidence": round(conf, 4),
        "box": [x1, y1, x2, y2],
        "is_recent": is_recent,
    }
