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


def take_chart_screenshot(page: Page, ticker: str) -> bool:
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
                if locator.count() > 0 and locator.first.is_visible():
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
            chart_element.screenshot(path=str(filepath))
            print(f"[screenshot] ✅ Saved chart screenshot: {filepath}")
        else:
            # Fallback: screenshot the full viewport if chart container not found
            print("[screenshot] WARNING: Chart container not found, taking full viewport screenshot.")
            page.screenshot(path=str(filepath), full_page=False)
            print(f"[screenshot] ✅ Saved full viewport screenshot: {filepath}")

        return True

    except Exception as e:
        print(f"[screenshot] ❌ ERROR capturing screenshot for {ticker}: {e}")
        return False
