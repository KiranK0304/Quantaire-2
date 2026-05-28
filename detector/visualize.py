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


def draw_and_save(
    image: str | Path | np.ndarray,
    detection: dict,
    output_dir: Path | None = None,
) -> str | None:
    """
    Draw detection box, label, and coordinates on the image and save it.

    Args:
        image:      Path to the original chart screenshot, OR a numpy array (BGR).
        detection:  Detection dict from inference.run_inference().
        output_dir: Directory to save the annotated image. Defaults to ANNOTATED_DIR.

    Returns:
        Path to the saved annotated image, or None if no detection / error.
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
