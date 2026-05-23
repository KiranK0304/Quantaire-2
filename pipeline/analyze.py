"""
pipeline/analyze.py — Single-stock analysis entry point.

Takes a single stock ticker, captures its chart from TradingView,
runs YOLO inference in-memory (no raw screenshot saved to disk),
and saves only the annotated output.

Usage:
    uv run python -m pipeline.analyze RELIANCE
    uv run python -m pipeline.analyze TCS
    uv run python -m pipeline.analyze RELIANCE --show    # preview the screenshot before inference
"""

import sys

import cv2
import numpy as np
from playwright.sync_api import sync_playwright

from configs.settings import ANALYZED_DIR
from tradingview.browser import launch_browser, open_tradingview, close_browser
from tradingview.capture import capture_ticker_chart
from detector.inference import run_inference
from detector.visualize import draw_and_save


def analyze_single(ticker: str, show_image: bool = False) -> dict | None:
    """
    Full pipeline for a single stock: screenshot → inference → annotated output.

    Steps:
      1. Launch browser and open TradingView
      2. Capture chart using the shared core function (search → timeframe → zoom → screenshot)
      3. Close browser
      4. Decode PNG bytes to numpy array
      5. Run YOLO inference on the numpy array
      6. Save annotated image to screenshots/analyzed/
      7. Print results

    Args:
        ticker: Stock symbol (e.g. "RELIANCE", "TCS").

    Returns:
        Detection result dict, or None if the process failed.
    """

    ticker = ticker.strip().upper()

    print("\n" + "=" * 60)
    print(f"  Single Stock Analysis — {ticker}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Phase 1: Capture chart screenshot to memory
    # ------------------------------------------------------------------
    print("\n  Phase 1: Capturing chart from TradingView...")

    png_bytes = None

    with sync_playwright() as playwright:
        browser, context, page = launch_browser(playwright)

        try:
            open_tradingview(page)

            # Use the same core function as the batch scanner
            png_bytes = capture_ticker_chart(page, ticker)

        finally:
            close_browser(browser)

    if png_bytes is None:
        print("\n  ❌ FAILED: Could not capture chart screenshot.")
        return None

    # ------------------------------------------------------------------
    # Phase 2: Decode PNG bytes to numpy array
    # ------------------------------------------------------------------

    # Decode PNG bytes → numpy array (BGR, as OpenCV expects)
    img_array = cv2.imdecode(
        np.frombuffer(png_bytes, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if img_array is None:
        print("\n  ❌ FAILED: Could not decode screenshot bytes.")
        return None

    # ------------------------------------------------------------------
    # Phase 2b: Optionally show the captured image for visual confirmation
    # ------------------------------------------------------------------
    if show_image:
        import matplotlib.pyplot as plt

        print("\n  Showing captured screenshot (close window to continue)...")
        rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(16, 9))
        plt.imshow(rgb)
        plt.title(f"Captured Chart — {ticker}", fontsize=18)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------------
    # Phase 3: Run YOLO inference on the in-memory image
    # ------------------------------------------------------------------
    print("\n  Phase 3: Running YOLO inference...")
    result = run_inference(img_array, ticker)

    # ------------------------------------------------------------------
    # Phase 4: Print results and save annotated image
    # ------------------------------------------------------------------
    print(f"\n{'=' * 55}")
    print(f"  Result: {ticker}")
    print(f"{'=' * 55}")

    if result["detected"]:
        x1, y1, x2, y2 = result["box"]

        print(f"  Pattern      : {result['label']}")
        print(f"  Confidence   : {result['confidence']:.2f}")
        print(f"  Coordinates  : ({x1},{y1}) → ({x2},{y2})")
        print(f"  Total boxes  : {result['all_count']}")

        # Draw and save annotated image to screenshots/analyzed/
        output_path = draw_and_save(img_array, result, output_dir=ANALYZED_DIR)

        if output_path:
            print(f"  Saved Output : {output_path}")
            result["output_path"] = output_path
        else:
            print(f"  Saved Output : FAILED")
    else:
        print(f"  No pattern detected.")

    print("=" * 55)
    print()

    return result


def main():
    """CLI entry point."""

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print("Usage: uv run python -m pipeline.analyze <TICKER> [--show]")
        print("Example: uv run python -m pipeline.analyze RELIANCE --show")
        sys.exit(1)

    ticker = args[0]
    show_image = "--show" in flags

    analyze_single(ticker, show_image=show_image)


if __name__ == "__main__":
    main()
