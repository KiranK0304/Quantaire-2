"""
visualize.py — Detection visualization and annotated image saving.

Draws detection boxes, labels, and coordinates onto the chart image
and saves the annotated result.
"""

import cv2
import numpy as np
from pathlib import Path

from configs.settings import ANNOTATED_DIR


# --------------------------------------------------------------------------
# Drawing constants & Colors
# --------------------------------------------------------------------------

# Define colors (BGR format for OpenCV)
COLORS = {
    "bullish": (100, 200, 100),   # Soft Green
    "bearish": (100, 100, 255),   # Soft Red
    "neutral": (255, 170, 100),   # Soft Blue
    "default": (200, 200, 200)    # Gray
}

def get_pattern_color(label: str) -> tuple:
    label_lower = label.lower()
    if "bottom" in label_lower or "w_head" in label_lower:
        return COLORS["bullish"]
    elif "top" in label_lower or "m_head" in label_lower:
        return COLORS["bearish"]
    elif "triangle" in label_lower:
        return COLORS["neutral"]
    return COLORS["default"]

def draw_and_save(
    image: str | Path | np.ndarray,
    detection: dict,
    output_dir: Path | None = None,
) -> str | None:
    """
    Draw detection box, label, and coordinates on the image and save it.
    """

    if not detection.get("detected"):
        return None

    try:
        # Load or use the image
        if isinstance(image, np.ndarray):
            img = image.copy()
        else:
            img = cv2.imread(str(image))
            if img is None:
                print(f"[visualize] ERROR: Could not read image: {image}")
                return None

        ticker = detection["ticker"]
        label = detection["label"]
        conf = detection["confidence"]
        x1, y1, x2, y2 = detection["box"]

        color = get_pattern_color(label)

        # ------------------------------------------------------------------
        # 1. Draw Translucent Overlay
        # ------------------------------------------------------------------
        overlay = img.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
        
        # Blend overlay with original image
        alpha = 0.25
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        # Draw a clean, thin solid border
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # ------------------------------------------------------------------
        # 2. Draw Label Badge
        # ------------------------------------------------------------------
        label_text = f"{label} ({int(conf * 100)}%)"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        
        # Get text size to draw the background box
        (text_width, text_height), baseline = cv2.getTextSize(label_text, font, font_scale, thickness)
        
        padding = 8
        badge_x1 = x1
        badge_y1 = max(0, y1 - text_height - (padding * 2))
        badge_x2 = x1 + text_width + (padding * 2)
        badge_y2 = y1
        
        # Draw badge background
        cv2.rectangle(img, (badge_x1, badge_y1), (badge_x2, badge_y2), color, -1)
        
        # Draw white text over the badge for high contrast
        cv2.putText(img, label_text, (badge_x1 + padding, badge_y2 - padding), font, font_scale, (255, 255, 255), thickness)

        # ------------------------------------------------------------------
        # Save annotated image
        # ------------------------------------------------------------------
        timeframe = detection.get("timeframe", "1D")
        is_recent = detection.get("is_recent", False)
        subfolder = "recent" if is_recent else "historical"

        save_dir = output_dir or (ANNOTATED_DIR / timeframe / subfolder)
        save_dir.mkdir(parents=True, exist_ok=True)
        output_path = save_dir / f"{ticker}_{timeframe}_detected.png"

        cv2.imwrite(str(output_path), img)
        return str(output_path)

    except Exception as e:
        print(f"[visualize] ERROR drawing on image: {e}")
        return None
