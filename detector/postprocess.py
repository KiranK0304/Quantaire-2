"""
postprocess.py — Detection post-processing helpers.

Lightweight helper functions for:
  - Selecting the rightmost/latest detection box
  - Filtering low-confidence detections
  - Converting YOLO output to a clean dictionary
"""


def select_rightmost_box(boxes):
    """
    Select the rightmost (latest in time) detection box.

    On a stock chart, the rightmost box corresponds to the most recent
    pattern formation, which is what we care about.

    Args:
        boxes: YOLO boxes object (results[0].boxes).

    Returns:
        The single box with the largest x2 coordinate, or None if empty.
    """

    if boxes is None or len(boxes) == 0:
        return None

    # x2 (right edge) is at index 2 of xyxy coordinates
    rightmost = max(boxes, key=lambda b: b.xyxy[0][2].item())
    return rightmost


def filter_by_confidence(boxes, min_conf: float = 0.2):
    """
    Filter detection boxes by minimum confidence threshold.

    Args:
        boxes:    YOLO boxes object.
        min_conf: Minimum confidence score (default 0.2).

    Returns:
        List of boxes above the confidence threshold.
    """

    if boxes is None or len(boxes) == 0:
        return []

    return [b for b in boxes if float(b.conf[0]) >= min_conf]


def box_to_dict(box, model_names: dict, ticker: str) -> dict:
    """
    Convert a single YOLO detection box into a clean dictionary.

    Args:
        box:         A single YOLO box object.
        model_names: The model.names dict mapping class IDs to label strings.
        ticker:      The stock ticker this detection belongs to.

    Returns:
        Dictionary with keys: ticker, label, confidence, box
    """

    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    label = model_names[cls_id]

    x1, y1, x2, y2 = map(int, box.xyxy[0])

    return {
        "ticker": ticker,
        "label": label,
        "confidence": round(conf, 4),
        "box": [x1, y1, x2, y2],
    }
