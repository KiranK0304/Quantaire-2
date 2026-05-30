"""
settings.py — Central project paths and configuration.

All paths are relative to the project root.
Keeps path logic in one place so modules don't hardcode paths.
"""

from pathlib import Path


# --------------------------------------------------------------------------
# Project root (2 levels up from configs/settings.py)
# --------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# YOLO Model
# --------------------------------------------------------------------------

MODEL_PATH = PROJECT_ROOT / "stockmarket-pattern-detection-yolov8" / "model.pt"

# Minimum confidence threshold for detections
CONFIDENCE_THRESHOLD = 0.2

# --------------------------------------------------------------------------
# Cropped Inference Configuration
# --------------------------------------------------------------------------

# Analyzes only the right-side portion of the chart (e.g., 0.5 = 50%, 0.3 = 30%)
CROP_INFERENCE_RATIO = 0.5

# Save the intermediate cropped image for debugging/verification
SAVE_CROP_IMAGES = False

# Box must be in the rightmost 15% of the chart to be considered "recent/active"
RECENCY_THRESHOLD_PERCENT = 0.15

# Batch scanner configuration (Single screenshot per stock)
BATCH_DATE_RANGE = "6M"
BATCH_CANDLE_TF = "2h"

# --------------------------------------------------------------------------
# Input / Output Directories
# --------------------------------------------------------------------------

SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# Single-stock analysis saves annotated output here (no raw screenshot saved)
ANALYZED_DIR = SCREENSHOTS_DIR / "analyzed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ANNOTATED_DIR = OUTPUTS_DIR / "annotated"
LOGS_DIR = OUTPUTS_DIR / "logs"
SINGLE_STOCK_DIR = OUTPUTS_DIR / "single_stock"
