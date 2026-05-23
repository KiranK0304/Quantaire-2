"""
capture.py — Core single-ticker capture function.

This is THE ONE function that both the batch scanner and the single-stock
analysis pipeline call. It handles the full TradingView interaction for
one ticker: state reset → popups → search → timeframe → zoom → capture.

Having one function ensures:
  - Identical behavior in batch and single modes
  - State cleanup between tickers (prevents stale focus/dialog bugs)
  - DRY — no duplicate search/timeframe/zoom logic
"""

from playwright.sync_api import Page

from tradingview.browser import dismiss_popups
from tradingview.search import search_ticker
from tradingview.timeframe import set_daily_timeframe, zoom_out_chart
from tradingview.screenshot import capture_chart_to_bytes


def _reset_chart_state(page: Page) -> None:
    """
    Reset the page to a clean state before processing a new ticker.

    This is critical for the batch scanner where the page is reused
    across 50+ tickers. After timeframe shortcuts and mouse wheel zoom,
    keyboard focus can land on random toolbar elements, causing the next
    search to fail.

    Steps:
      1. Press Escape to close any lingering dialog/dropdown/menu
      2. Click the chart body to move keyboard focus off toolbar buttons
      3. Brief pause to let the UI settle
    """

    try:
        # Close any open dialog/dropdown/overlay
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # Click the chart canvas to reset focus
        chart = page.locator('.layout__area--center')
        if chart.count() > 0 and chart.first.is_visible():
            chart.first.click(position={"x": 400, "y": 300})
            page.wait_for_timeout(300)
        else:
            # Fallback: click any canvas
            canvas = page.locator("canvas")
            if canvas.count() > 0:
                canvas.first.click()
                page.wait_for_timeout(300)

    except Exception:
        pass


def capture_ticker_chart(page: Page, ticker: str) -> bytes | None:
    """
    Process a single ticker on an already-open TradingView chart page.

    This function does NOT manage the browser session — it expects
    a `page` that is already on the TradingView chart page.

    Steps:
      1. Reset state (Escape + click chart body)
      2. Dismiss popups (login, ads, cookies)
      3. Search for the ticker
      4. Set timeframe to Daily (1D)
      5. Zoom out to show more candles
      6. Wait for chart to settle
      7. Capture chart screenshot to PNG bytes

    Args:
        page:   An active Playwright page on TradingView /chart/.
        ticker: Stock symbol (e.g. "RELIANCE", "TCS").

    Returns:
        PNG bytes of the chart screenshot, or None if any step failed.
    """

    # ------------------------------------------------------------------
    # Step 1: Reset to clean state
    # ------------------------------------------------------------------
    # This is the key robustness fix. Without this, stale focus from
    # the previous ticker's timeframe/zoom can break the next search.
    _reset_chart_state(page)

    # ------------------------------------------------------------------
    # Step 2: Dismiss any popups
    # ------------------------------------------------------------------
    dismiss_popups(page)

    # ------------------------------------------------------------------
    # Step 3: Search for the ticker
    # ------------------------------------------------------------------
    if not search_ticker(page, ticker):
        print(f"[capture] ❌ Search failed for '{ticker}'.")
        return None

    # ------------------------------------------------------------------
    # Step 4: Set timeframe to Daily
    # ------------------------------------------------------------------
    set_daily_timeframe(page)

    # ------------------------------------------------------------------
    # Step 5: Zoom out for more candles
    # ------------------------------------------------------------------
    zoom_out_chart(page, steps=3)

    # ------------------------------------------------------------------
    # Step 6: Let the chart fully settle after zoom
    # ------------------------------------------------------------------
    page.wait_for_timeout(1000)

    # ------------------------------------------------------------------
    # Step 7: Capture chart to bytes
    # ------------------------------------------------------------------
    png_bytes = capture_chart_to_bytes(page)

    if png_bytes is None:
        print(f"[capture] ❌ Screenshot capture failed for '{ticker}'.")
        return None

    return png_bytes
