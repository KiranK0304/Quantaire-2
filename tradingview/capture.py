"""
capture.py — Core single-ticker capture function.

Handles the full TradingView interaction for one ticker.
"""

from playwright.async_api import Page

from tradingview.browser import dismiss_popups
from tradingview.search import search_ticker
from tradingview.timeframe import set_timeframe, set_date_range, zoom_out_chart
from tradingview.screenshot import capture_chart_to_bytes


async def _reset_chart_state(page: Page) -> None:
    """Reset the page to a clean state before processing a new ticker."""
    try:
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        chart = page.locator('.layout__area--center')
        if await chart.count() > 0 and await chart.first.is_visible():
            await chart.first.click(position={"x": 400, "y": 300})
            await page.wait_for_timeout(300)
        else:
            canvas = page.locator("canvas")
            if await canvas.count() > 0:
                await canvas.first.click()
                await page.wait_for_timeout(300)

    except Exception:
        pass


async def capture_ticker_chart(page: Page, ticker: str, timeframe: str = "1D", date_range: str | None = None) -> bytes | None:
    """Search for a ticker, set timeframe/range, and capture screenshot."""

    await _reset_chart_state(page)
    await dismiss_popups(page)

    if not await search_ticker(page, ticker):
        print(f"[capture] ❌ Search failed for '{ticker}'.")
        return None

    if date_range:
        await set_date_range(page, date_range)
    else:
        await set_timeframe(page, timeframe)
        await zoom_out_chart(page, steps=3)

    await page.wait_for_timeout(1000)

    png_bytes = await capture_chart_to_bytes(page)

    if png_bytes is None:
        print(f"[capture] ❌ Screenshot capture failed for '{ticker}'.")
        return None

    return png_bytes


async def capture_chart_range(page: Page, date_range: str, candle_tf: str = "1D") -> bytes | None:
    """
    Change the candle timeframe and date range, then capture screenshot.
    Assumes the ticker is ALREADY loaded on the chart.
    Used by multi-range loop to avoid re-searching.
    """
    await _reset_chart_state(page)
    await dismiss_popups(page)

    await set_timeframe(page, candle_tf)
    await page.wait_for_timeout(500)

    await set_date_range(page, date_range)
    await page.wait_for_timeout(1000)

    png_bytes = await capture_chart_to_bytes(page)

    if png_bytes is None:
        print(f"[capture] ❌ Screenshot capture failed for range '{date_range}'.")
        return None

    return png_bytes
