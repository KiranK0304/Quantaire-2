"""
pipeline/main.py — Full pipeline orchestration.

Runs the optional Market Data scanner, followed by YOLO detection on all screenshots.
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
    """Run YOLO inference on all screenshots in the screenshots/ folder."""

    print("\n" + "=" * 60)
    print("  YOLO Detection Pipeline — Starting")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: Find all screenshots
    # ------------------------------------------------------------------
    screenshots = sorted(SCREENSHOTS_DIR.glob("*.png"))

    if not screenshots:
        print(f"\n  No screenshots found in {SCREENSHOTS_DIR}")
        print("  Run the Chart scanner first:")
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
        # Extract ticker and timeframe from filename (e.g. RELIANCE_1D.png)
        stem_parts = img_path.stem.split('_')
        ticker = stem_parts[0]
        timeframe = stem_parts[1] if len(stem_parts) > 1 else "1D"

        print(f"\n{'=' * 55}")
        print(f"  Processing: {img_path.name}")
        print(f"{'=' * 55}")

        result = run_inference(img_path, ticker, timeframe)

        if result["detected"]:
            detected_count += 1
            x1, y1, x2, y2 = result["box"]
            recency_str = "[RECENT]" if result.get("is_recent") else "[HISTORICAL]"

            print(f"  Pattern      : {result['label']} {recency_str}")
            print(f"  Timeframe    : {timeframe}")
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
    """Save detection results as a JSON log file."""
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = LOGS_DIR / f"detection_{timestamp}.json"

        serializable = []
        for r in results:
            entry = {
                "ticker": r["ticker"],
                "timeframe": r.get("timeframe", "1D"),
                "label": r["label"],
                "confidence": r["confidence"],
                "box": r["box"],
                "detected": r["detected"],
                "all_count": r["all_count"],
                "is_recent": r.get("is_recent", False),
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
    Entry point. Optionally runs the Chart scanner first.
    """

    # Check if --with-scanner flag is passed
    if "--with-scanner" in sys.argv:
        print("[pipeline] Running Chart scanner first...")
        from tradingview.run_scanner import run as run_scanner
        run_scanner()

    # Run detection
    run_detection_pipeline()


if __name__ == "__main__":
    main()
