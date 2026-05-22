"""
pipeline/main.py — Full pipeline orchestration.

Workflow:
  1. (Optional) Run TradingView screenshot pipeline
  2. Load YOLO model
  3. Iterate through all screenshots
  4. Run inference on each image
  5. Save annotated images
  6. Print clean terminal output
  7. Save results log

Usage:
    python -m pipeline.main                   # detection only (screenshots must exist)
    python -m pipeline.main --with-scanner    # run scanner first, then detect
"""

import sys
import json
from datetime import datetime
from pathlib import Path

from configs.settings import SCREENSHOTS_DIR, ANNOTATED_DIR, LOGS_DIR
from detector.model import load_model
from detector.inference import run_inference
from detector.visualize import draw_and_save


def run_detection_pipeline() -> list[dict]:
    """
    Run YOLO inference on all screenshots in the screenshots/ folder.

    Returns:
        List of detection result dictionaries.
    """

    print("\n" + "=" * 60)
    print("  YOLO Detection Pipeline — Starting")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: Find all screenshots
    # ------------------------------------------------------------------
    screenshots = sorted(SCREENSHOTS_DIR.glob("*.png"))

    if not screenshots:
        print(f"\n  No screenshots found in {SCREENSHOTS_DIR}")
        print("  Run the TradingView scanner first:")
        print("    uv run python -m tradingview.run_scanner")
        print("=" * 60)
        return []

    print(f"  Screenshots found: {len(screenshots)}")
    print(f"  Output directory:  {ANNOTATED_DIR}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 2: Load model (once)
    # ------------------------------------------------------------------
    model = load_model()

    # ------------------------------------------------------------------
    # Step 3: Process each screenshot
    # ------------------------------------------------------------------
    all_results = []
    detected_count = 0

    for i, img_path in enumerate(screenshots, start=1):
        ticker = img_path.stem  # "RELIANCE.png" → "RELIANCE"

        print(f"\n{'=' * 55}")
        print(f"  Processing: {img_path.name}")
        print(f"{'=' * 55}")

        # Run inference
        result = run_inference(img_path, ticker)

        if result["detected"]:
            detected_count += 1
            x1, y1, x2, y2 = result["box"]

            print(f"  Pattern      : {result['label']}")
            print(f"  Confidence   : {result['confidence']:.2f}")
            print(f"  Coordinates  : ({x1},{y1}) → ({x2},{y2})")
            print(f"  Total boxes  : {result['all_count']}")

            # Draw and save annotated image
            output_path = draw_and_save(img_path, result)

            if output_path:
                print(f"  Saved Output : {output_path}")
                result["output_path"] = output_path
            else:
                print(f"  Saved Output : FAILED")

        else:
            print(f"  No pattern detected")

        all_results.append(result)

    # ------------------------------------------------------------------
    # Step 4: Save results log
    # ------------------------------------------------------------------
    _save_results_log(all_results)

    # ------------------------------------------------------------------
    # Step 5: Print summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  DETECTION COMPLETE")
    print("=" * 60)
    print(f"  Total images     : {len(screenshots)}")
    print(f"  Patterns found   : {detected_count}")
    print(f"  No detection     : {len(screenshots) - detected_count}")
    print(f"  Annotated images : {ANNOTATED_DIR}")
    print("=" * 60)

    # Print results table
    if all_results:
        print(f"\n  {'Ticker':<12} {'Pattern':<20} {'Confidence':<12} {'Box'}")
        print(f"  {'—'*12} {'—'*20} {'—'*12} {'—'*25}")
        for r in all_results:
            if r["detected"]:
                x1, y1, x2, y2 = r["box"]
                print(f"  {r['ticker']:<12} {r['label']:<20} {r['confidence']:<12.2f} ({x1},{y1})→({x2},{y2})")
            else:
                print(f"  {r['ticker']:<12} {'—':<20} {'—':<12} —")

    print()
    return all_results


def _save_results_log(results: list[dict]) -> None:
    """
    Save detection results as a JSON log file.

    Filename includes timestamp so logs don't overwrite each other.
    """

    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = LOGS_DIR / f"detection_{timestamp}.json"

        # Make results JSON-serializable (remove non-serializable fields)
        serializable = []
        for r in results:
            entry = {
                "ticker": r["ticker"],
                "label": r["label"],
                "confidence": r["confidence"],
                "box": r["box"],
                "detected": r["detected"],
                "all_count": r["all_count"],
            }
            if "output_path" in r:
                entry["output_path"] = r["output_path"]
            serializable.append(entry)

        with open(log_path, "w") as f:
            json.dump(serializable, f, indent=2)

        print(f"\n  Log saved: {log_path}")

    except Exception as e:
        print(f"\n  WARNING: Could not save log: {e}")


def main():
    """
    Entry point. Optionally runs the TradingView scanner first.
    """

    # Check if --with-scanner flag is passed
    if "--with-scanner" in sys.argv:
        print("[pipeline] Running TradingView scanner first...")
        from tradingview.run_scanner import run as run_scanner
        run_scanner()

    # Run detection
    run_detection_pipeline()


if __name__ == "__main__":
    main()
