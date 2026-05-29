"""
pipeline/analyze.py — Single-stock analysis entry point.

Usage:
    uv run python -m pipeline.analyze RELIANCE
    uv run python -m pipeline.analyze TCS 1W
    uv run python -m pipeline.analyze RELIANCE 1h --show
"""

import sys
import json
import cv2
import numpy as np
from pathlib import Path
from playwright.async_api import async_playwright
import asyncio

from configs.settings import ANALYZED_DIR, SINGLE_STOCK_DIR, CROP_INFERENCE_RATIO, SAVE_CROP_IMAGES
from tradingview.browser import launch_browser, open_tradingview, close_browser
from tradingview.capture import capture_ticker_chart, capture_chart_range
from tradingview.search import search_ticker
from detector.inference import run_inference
from detector.visualize import draw_and_save


def _get_next_run_folder() -> Path:
    """Find the next sequential run_XXX folder in single_stock_dir."""
    SINGLE_STOCK_DIR.mkdir(parents=True, exist_ok=True)
    
    existing_runs = [d for d in SINGLE_STOCK_DIR.iterdir() if d.is_dir() and d.name.startswith("run_")]
    if not existing_runs:
        next_run = "run_001"
    else:
        nums = []
        for d in existing_runs:
            try:
                nums.append(int(d.name.split("_")[1]))
            except ValueError:
                pass
        next_num = max(nums) + 1 if nums else 1
        next_run = f"run_{next_num:03d}"
        
    run_dir = SINGLE_STOCK_DIR / next_run
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


async def analyze_single(ticker: str, timeframe: str = "1D", show_image: bool = False, multi_range: bool = False) -> list[dict] | dict | None:
    """Full pipeline for a single stock: screenshot → inference → annotated output."""

    ticker = ticker.strip().upper()

    print("\n" + "=" * 60)
    print(f"  Single Stock Analysis — {ticker}")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Phase 1: Capture chart screenshot to memory
    # ------------------------------------------------------------------
    print("\n  Phase 1: Capturing chart from Market Data Provider...")

    png_bytes = None


    async with async_playwright() as playwright:
        browser, context, _ = await launch_browser(playwright)

        try:
            if multi_range:
                ranges = ["1M", "3M", "6M", "1Y"]
                run_folder = _get_next_run_folder()
                print(f"\n  [info] Saving multi-range outputs to: {run_folder.name}")

                async def process_range(dr: str):
                    candle_tf = "1D"
                    if dr == "1M":
                        candle_tf = "15"
                    elif dr == "3M":
                        candle_tf = "1h"
                    elif dr == "6M":
                        candle_tf = "2h"

                    print(f"  --- Launching parallel capture for: {dr} ---")
                    page = await context.new_page()
                    try:
                        await open_tradingview(page)
                        png_data = await capture_ticker_chart(page, ticker, timeframe=candle_tf, date_range=dr)
                        
                        if not png_data:
                            print(f"  ❌ Capture failed for range {dr}.")
                            return None
                        
                        img_array = cv2.imdecode(np.frombuffer(png_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                        height, width = img_array.shape[:2]
                        crop_start_x = int(width * (1.0 - CROP_INFERENCE_RATIO))
                        crop_img = img_array[:, crop_start_x:]
                        
                        if SAVE_CROP_IMAGES:
                            crop_path = run_folder / f"{ticker}_{dr}_crop.png"
                            cv2.imwrite(str(crop_path), crop_img)
                            
                        res = run_inference(crop_img, ticker, timeframe=dr)
                        if res["detected"]:
                            res["box"][0] += crop_start_x
                            res["box"][2] += crop_start_x
                            output_path = draw_and_save(img_array, res, output_dir=run_folder)
                            res["output_path"] = output_path
                            print(f"  ✅ Pattern [{dr}]: {res['label']} ({res['confidence']:.2f})")
                        else:
                            output_path = run_folder / f"{ticker}_{dr}_detected.png"
                            cv2.imwrite(str(output_path), img_array)
                            res["output_path"] = str(output_path)
                            print(f"  ⚪ No pattern [{dr}]. Clean chart saved.")
                            
                        return res
                    finally:
                        await page.close()

                # Run all timeframes concurrently
                tasks = [process_range(dr) for dr in ranges]
                results = await asyncio.gather(*tasks)
                
                valid_results = [r for r in results if r is not None]
                print("\n" + "=" * 60)
                return valid_results

            else:
                # Original single timeframe logic
                page = await context.new_page()
                await open_tradingview(page)
                png_bytes = await capture_ticker_chart(page, ticker, timeframe)

                if png_bytes is None:
                    print("\n  ❌ FAILED: Could not capture chart screenshot.")
                    await page.close()
                    return None

                img_array = cv2.imdecode(np.frombuffer(png_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

                # --- Cropped Inference Strategy ---
                height, width = img_array.shape[:2]
                crop_start_x = int(width * (1.0 - CROP_INFERENCE_RATIO))
                crop_img = img_array[:, crop_start_x:]
                
                if SAVE_CROP_IMAGES:
                    crop_path = ANALYZED_DIR / f"{ticker}_crop.png"
                    crop_path.parent.mkdir(parents=True, exist_ok=True)
                    cv2.imwrite(str(crop_path), crop_img)

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

                print("\n  Phase 3: Running YOLO inference on cropped region...")
                result = run_inference(crop_img, ticker, timeframe)

                print(f"\n{'=' * 55}")
                print(f"  Result: {ticker}")
                print(f"{'=' * 55}")

                if result["detected"]:
                    # Map coordinates back to the full image
                    result["box"][0] += crop_start_x
                    result["box"][2] += crop_start_x
                    
                    x1, y1, x2, y2 = result["box"]
                    print(f"  Pattern      : {result['label']}")
                    print(f"  Confidence   : {result['confidence']:.2f}")
                    print(f"  Coordinates  : ({x1},{y1}) → ({x2},{y2})")
                    print(f"  Total boxes  : {result['all_count']}")

                    # Draw on FULL image
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
                await page.close()
                return result

        finally:
            await close_browser(browser)


def main():
    """CLI entry point."""

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    if not args:
        print("Usage: uv run python -m pipeline.analyze <TICKER> [TIMEFRAME] [--show] [--multi-range]")
        print("Example: uv run python -m pipeline.analyze RELIANCE 1W --show")
        print("Example: uv run python -m pipeline.analyze RELIANCE --multi-range")
        sys.exit(1)

    ticker = args[0]
    timeframe = args[1] if len(args) > 1 else "1D"
    show_image = "--show" in flags
    multi_range = "--multi-range" in flags

    asyncio.run(analyze_single(ticker, timeframe=timeframe, show_image=show_image, multi_range=multi_range))


if __name__ == "__main__":
    main()
