"""
run_scanner.py — Main orchestration script.

This is the entry point for the TradingView screenshot automation.
It loops through a list of stock tickers, searches each one on TradingView,
sets the timeframe to Daily, and captures a clean chart screenshot.

Usage:
    python -m tradingview.run_scanner
"""

from playwright.async_api import async_playwright
import asyncio
import time
import json
from datetime import datetime

from configs.settings import LOGS_DIR, SCREENSHOTS_DIR, BATCH_DATE_RANGE, BATCH_CANDLE_TF

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


async def run():
    """Main scanner loop across multiple timeframes."""

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

    async with async_playwright() as playwright:
        browser, context, page = await launch_browser(playwright)
        await open_tradingview(page)

        print(f"\n" + "=" * 60)
        print(f"  Starting single-range batch scan: {BATCH_DATE_RANGE} with {BATCH_CANDLE_TF} candles")
        print("=" * 60)

        for i, ticker in enumerate(STOCKS, start=1):
            log_entry = {
                "ticker": ticker,
                "timeframe": BATCH_DATE_RANGE,
                "status": "success",
                "reason": "OK"
            }

            print(f"\n{'—' * 50}")
            print(f"  [{i}/{len(STOCKS)}] Processing: {ticker} ({BATCH_DATE_RANGE})")
            print(f"{'—' * 50}")

            png_bytes = await capture_ticker_chart(page, ticker, timeframe=BATCH_CANDLE_TF, date_range=BATCH_DATE_RANGE)

            if not png_bytes:
                print(f"  Capture failed for {ticker}. Launching fresh browser session and retrying...")
                await close_browser(browser)
                browser, context, page = await launch_browser(playwright)
                await open_tradingview(page)
                png_bytes = await capture_ticker_chart(page, ticker, timeframe=BATCH_CANDLE_TF, date_range=BATCH_DATE_RANGE)

            if png_bytes:
                SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
                save_path = SCREENSHOTS_DIR / f"{ticker}_{BATCH_DATE_RANGE}.png"
                save_path.write_bytes(png_bytes)
                print(f"  ✅ Saved: {save_path}")
                success.append(f"{ticker}_{BATCH_DATE_RANGE}")
                
                log_entry["status"] = "success"
                log_entry["reason"] = "OK"
            else:
                failed.append(f"{ticker}_{BATCH_DATE_RANGE}")
                log_entry["status"] = "failed"
                log_entry["reason"] = "Capture failed even after retry"

            scanner_logs.append(log_entry)

            if i < len(STOCKS):
                print(f"  Waiting {DELAY_BETWEEN_STOCKS}s before next ticker...")
                await asyncio.sleep(DELAY_BETWEEN_STOCKS)

        await close_browser(browser)

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
    asyncio.run(run())
