"""
visualize.py — Detection visualization and annotated image saving.

Draws detection boxes, labels, and coordinates onto the chart image
and saves the annotated result.
"""

import cv2
from pathlib import Path

from configs.settings import ANNOTATED_DIR


# --------------------------------------------------------------------------
# Drawing constants
# --------------------------------------------------------------------------

# Colors (BGR format for OpenCV)
BOX_COLOR = (255, 0, 255)       # Magenta — thick detection box
LABEL_COLOR = (255, 0, 255)     # Magenta — label text
TOP_LEFT_COLOR = (0, 255, 0)    # Green — top-left corner marker
BOTTOM_RIGHT_COLOR = (0, 0, 255)  # Red — bottom-right corner marker

BOX_THICKNESS = 4
CORNER_RADIUS = 8
LABEL_FONT_SCALE = 1.0
LABEL_THICKNESS = 3
COORD_FONT_SCALE = 0.8
COORD_THICKNESS = 2


def draw_and_save(image_path: str | Path, detection: dict) -> str | None:
    """
    Draw detection box, label, and coordinates on the image and save it.

    Args:
        image_path: Path to the original chart screenshot.
        detection:  Detection dict from inference.run_inference().

    Returns:
        Path to the saved annotated image, or None if no detection / error.
    """

    if not detection.get("detected"):
        return None

    try:
        # Read the original image
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"[visualize] ERROR: Could not read image: {image_path}")
            return None

        ticker = detection["ticker"]
        label = detection["label"]
        conf = detection["confidence"]
        x1, y1, x2, y2 = detection["box"]

        # ------------------------------------------------------------------
        # Draw detection box
        # ------------------------------------------------------------------
        cv2.rectangle(img, (x1, y1), (x2, y2), BOX_COLOR, BOX_THICKNESS)

        # ------------------------------------------------------------------
        # Draw corner circles
        # ------------------------------------------------------------------
        cv2.circle(img, (x1, y1), CORNER_RADIUS, TOP_LEFT_COLOR, -1)
        cv2.circle(img, (x2, y2), CORNER_RADIUS, BOTTOM_RIGHT_COLOR, -1)

        # ------------------------------------------------------------------
        # Draw label text above the box
        # ------------------------------------------------------------------
        label_text = f"{label} ({conf:.2f})"
        cv2.putText(
            img, label_text,
            (x1, y1 - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            LABEL_FONT_SCALE, LABEL_COLOR, LABEL_THICKNESS,
        )

        # ------------------------------------------------------------------
        # Draw coordinate text at corners
        # ------------------------------------------------------------------
        cv2.putText(
            img, f"({x1}, {y1})",
            (x1 + 10, y1 + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            COORD_FONT_SCALE, TOP_LEFT_COLOR, COORD_THICKNESS,
        )

        cv2.putText(
            img, f"({x2}, {y2})",
            (x2 - 160, y2 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            COORD_FONT_SCALE, BOTTOM_RIGHT_COLOR, COORD_THICKNESS,
        )

        # ------------------------------------------------------------------
        # Save annotated image
        # ------------------------------------------------------------------
        ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)
        output_path = ANNOTATED_DIR / f"{ticker}_detected.png"

        cv2.imwrite(str(output_path), img)
        return str(output_path)

    except Exception as e:
        print(f"[visualize] ERROR drawing on {image_path}: {e}")
        return None
