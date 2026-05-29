"""
screenshot.py — Chart screenshot capture logic.

Handles:
  - Locating the chart container element (NOT the full page)
  - Taking a screenshot of ONLY the chart area
  - Saving screenshots with consistent naming to the screenshots/ folder
"""

from playwright.sync_api import Page
from pathlib import Path


# --------------------------------------------------------------------------
# Screenshot output directory (relative to project root)
# --------------------------------------------------------------------------

SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "screenshots"


async def take_chart_screenshot(page: Page, ticker: str) -> bool:
    """
    Capture a screenshot of ONLY the chart area on TradingView.

    TradingView renders the chart inside a specific container element.
    We locate that container and screenshot just that element, avoiding
    toolbars, sidebars, and other UI clutter.

    Args:
        page:   The active Playwright page.
        ticker: Stock symbol used for the filename (e.g. "RELIANCE").

    Returns:
        True if screenshot was saved successfully, False otherwise.
    """

    print(f"[screenshot] Capturing chart for {ticker}...")

    try:
        # Ensure the screenshots directory exists
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

        # ------------------------------------------------------------------
        # Locate the chart container
        # ------------------------------------------------------------------
        # From live DOM inspection, these are the actual selectors that work
        # on TradingView's chart page (verified May 2026):
        #
        #   .layout__area--center     — the center layout area (chart only)
        #   [data-name="chart-container"]  — chart container data attribute
        #   .chart-markup-table       — the chart markup table

        chart_selectors = [
            '.layout__area--center',                  # center layout (chart only, no sidebar)
            '[data-name="chart-container"]',           # data attribute on chart container
            '.chart-markup-table',                     # chart markup table
            '.chart-container',                        # generic class
        ]

        chart_element = None

        for selector in chart_selectors:
            try:
                locator = page.locator(selector)
                if await locator.count() > 0 and await locator.first.is_visible():
                    chart_element = locator.first
                    print(f"[screenshot] Found chart using selector: {selector}")
                    break
            except Exception:
                continue

        # ------------------------------------------------------------------
        # Take the screenshot
        # ------------------------------------------------------------------

        filepath = SCREENSHOTS_DIR / f"{ticker}.png"

        if chart_element:
            # Screenshot ONLY the chart container element
            await chart_element.screenshot(path=str(filepath))
            print(f"[screenshot] ✅ Saved chart screenshot: {filepath}")
        else:
            # Fallback: screenshot the full viewport if chart container not found
            print("[screenshot] WARNING: Chart container not found, taking full viewport screenshot.")
            await page.screenshot(path=str(filepath), full_page=False)
            print(f"[screenshot] ✅ Saved full viewport screenshot: {filepath}")

        return True

    except Exception as e:
        print(f"[screenshot] ❌ ERROR capturing screenshot for {ticker}: {e}")
        return False


async def capture_chart_to_bytes(page: Page) -> bytes | None:
    """
    Capture a screenshot of the chart area and return it as PNG bytes.

    This does NOT save anything to disk. The bytes can be decoded into
    a numpy array for in-memory inference.

    Args:
        page: The active Playwright page.

    Returns:
        PNG image bytes, or None if the chart element could not be found.
    """

    print("[screenshot] Capturing chart to memory...")

    try:
        # Use the same selectors as take_chart_screenshot
        chart_selectors = [
            '.layout__area--center',
            '[data-name="chart-container"]',
            '.chart-markup-table',
            '.chart-container',
        ]

        for selector in chart_selectors:
            try:
                locator = page.locator(selector)
                if await locator.count() > 0 and await locator.first.is_visible():
                    png_bytes = await locator.first.screenshot()
                    print(f"[screenshot] ✅ Chart captured in memory ({len(png_bytes)} bytes)")
                    return png_bytes
            except Exception:
                continue

        # Fallback: full viewport screenshot
        print("[screenshot] WARNING: Chart container not found, capturing full viewport.")
        png_bytes = await page.screenshot(full_page=False)
        return png_bytes

    except Exception as e:
        print(f"[screenshot] ❌ ERROR capturing chart to memory: {e}")
        return None
