"""
run_scanner.py — Main orchestration script.

This is the entry point for the TradingView screenshot automation.
It loops through a list of stock tickers, searches each one on TradingView,
sets the timeframe to Daily, and captures a clean chart screenshot.

Usage:
    python -m tradingview.run_scanner
"""

from playwright.sync_api import sync_playwright
import time
import json
from datetime import datetime

from configs.settings import LOGS_DIR, SCREENSHOTS_DIR

from tradingview.browser import launch_browser, open_tradingview, close_browser
from tradingview.capture import capture_ticker_chart


# --------------------------------------------------------------------------
# Stock list — add/remove tickers here
# --------------------------------------------------------------------------

STOCKS = [
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BEL",
    "BHARTIARTL",
    "BPCL",
    "BRITANNIA",
    "CIPLA",
    "COALINDIA",
    "DIVISLAB",
    "DRREDDY",
    "EICHERMOT",
    "ETERNAL",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "INDUSINDBK",
    "INFY",
    "INDIGO",
    "ITC",
    "JSWSTEEL",
    "JIOFIN",
    "KOTAKBANK",
    "LT",
    "M&M",
    "MARUTI",
    "MAXHEALTH",
    "NESTLEIND",
    "NTPC",
    "ONGC",
    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SHRIRAMFIN",
    "SBIN",
    "SUNPHARMA",
    "TATAMOTORS",
    "TATASTEEL",
    "TCS",
    "TECHM",
    "TITAN",
    "TRENT",
    "ULTRACEMCO",
    "WIPRO",
]
# Delay between processing each ticker (seconds)
# Helps avoid rate-limiting and gives charts time to settle
DELAY_BETWEEN_STOCKS = 2


def run():
    """
    Main scanner loop.

    Workflow for each ticker:
      1. Search for the ticker
      2. Set timeframe to Daily
      3. Zoom out slightly for more candle visibility
      4. Take a chart-only screenshot
      5. Move on to the next ticker
    """

    print("=" * 60)
    print("  TradingView Chart Scanner — Starting")
    print("=" * 60)
    print(f"  Stocks to scan: {STOCKS}")
    print(f"  Total: {len(STOCKS)}")
    print("=" * 60)

    # Track results
    success = []
    failed = []
    scanner_logs = []

    with sync_playwright() as playwright:

        # Launch browser and open TradingView
        browser, context, page = launch_browser(playwright)
        open_tradingview(page)

        for i, ticker in enumerate(STOCKS, start=1):
            log_entry = {
                "ticker": ticker,
                "status": "success",
                "reason": "OK"
            }

            print(f"\n{'—' * 50}")
            print(f"  [{i}/{len(STOCKS)}] Processing: {ticker}")
            print(f"{'—' * 50}")

            # 1. Try to capture normally
            png_bytes = capture_ticker_chart(page, ticker)

            # 2. If it fails (likely due to signup overlay), launch fresh session
            if not png_bytes:
                print(f"  Capture failed for {ticker}. Launching fresh browser session and retrying...")
                
                # Force-close the blocked session
                close_browser(browser)
                
                # Launch a brand new incognito session
                browser, context, page = launch_browser(playwright)
                open_tradingview(page)
                
                # Retry capture
                png_bytes = capture_ticker_chart(page, ticker)

            # 3. Process results
            if png_bytes:
                # Save the captured bytes to disk
                SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
                save_path = SCREENSHOTS_DIR / f"{ticker}.png"
                save_path.write_bytes(png_bytes)
                print(f"  ✅ Saved: {save_path}")
                success.append(ticker)
                
                # If it succeeded on the retry, update the log entry status back to success
                log_entry["status"] = "success"
                log_entry["reason"] = "OK (after session recreation retry)"
            else:
                failed.append(ticker)
                log_entry["status"] = "failed"
                log_entry["reason"] = "Capture failed even after fresh session retry"

            scanner_logs.append(log_entry)

            # Pause before next ticker
            if i < len(STOCKS):
                print(f"  Waiting {DELAY_BETWEEN_STOCKS}s before next ticker...")
                time.sleep(DELAY_BETWEEN_STOCKS)

        # Done — close the browser
        close_browser(browser)

    # ------------------------------------------------------------------
    # Save Scanner Logs
    # ------------------------------------------------------------------
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = LOGS_DIR / f"scanner_{timestamp}.json"
        
        summary = {
            "total_scanned": len(STOCKS),
            "successful_count": len(success),
            "failed_count": len(failed),
            "logs": scanner_logs
        }
        
        with open(log_path, "w") as f:
            json.dump(summary, f, indent=2)
            
        print(f"\n  Scanner log saved to: {log_path}")
    except Exception as e:
        print(f"\n  WARNING: Could not save scanner log: {e}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    print("\n" + "=" * 60)
    print("  SCAN COMPLETE")
    print("=" * 60)
    print(f"  ✅ Success : {len(success)} — {success}")
    print(f"  ❌ Failed  : {len(failed)} — {failed}")
    print("=" * 60)


if __name__ == "__main__":
    run()
