"""
capture.py — Core single-ticker capture function.

Handles the full TradingView interaction for one ticker.
"""

from playwright.sync_api import Page

from tradingview.browser import dismiss_popups
from tradingview.search import search_ticker
from tradingview.timeframe import set_timeframe, set_date_range, zoom_out_chart
from tradingview.screenshot import capture_chart_to_bytes


def _reset_chart_state(page: Page) -> None:
    """Reset the page to a clean state before processing a new ticker."""
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        chart = page.locator('.layout__area--center')
        if chart.count() > 0 and chart.first.is_visible():
            chart.first.click(position={"x": 400, "y": 300})
            page.wait_for_timeout(300)
        else:
            canvas = page.locator("canvas")
            if canvas.count() > 0:
                canvas.first.click()
                page.wait_for_timeout(300)

    except Exception:
        pass


def capture_ticker_chart(page: Page, ticker: str, timeframe: str = "1D", date_range: str | None = None) -> bytes | None:
    """Search for a ticker, set timeframe/range, and capture screenshot."""

    _reset_chart_state(page)
    dismiss_popups(page)

    if not search_ticker(page, ticker):
        print(f"[capture] ❌ Search failed for '{ticker}'.")
        return None

    if date_range:
        set_date_range(page, date_range)
    else:
        set_timeframe(page, timeframe)
        zoom_out_chart(page, steps=3)

    page.wait_for_timeout(1000)

    png_bytes = capture_chart_to_bytes(page)

    if png_bytes is None:
        print(f"[capture] ❌ Screenshot capture failed for '{ticker}'.")
        return None

    return png_bytes


def capture_chart_range(page: Page, date_range: str, candle_tf: str = "1D") -> bytes | None:
    """
    Change the candle timeframe and date range, then capture screenshot.
    Assumes the ticker is ALREADY loaded on the chart.
    Used by multi-range loop to avoid re-searching.
    """
    _reset_chart_state(page)
    dismiss_popups(page)

    set_timeframe(page, candle_tf)
    page.wait_for_timeout(500)

    set_date_range(page, date_range)
    page.wait_for_timeout(1000)

    png_bytes = capture_chart_to_bytes(page)

    if png_bytes is None:
        print(f"[capture] ❌ Screenshot capture failed for range '{date_range}'.")
        return None

    return png_bytes
