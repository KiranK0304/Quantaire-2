"""
timeframe.py — Timeframe selection logic.

Handles:
  - Setting the chart timeframe to 1 Day (Daily)
  - Zooming out the chart to show more candles using mouse scroll

IMPORTANT:
  - Pressing just "D" on a chart opens symbol search and types "d" — WRONG.
  - Pressing "1" then "D" then "Enter" opens the timeframe dropdown and
    selects 1 Day — CORRECT.
  - Ctrl+Minus / Shift+ArrowLeft zoom the browser page, NOT the chart scale.
  - To zoom the chart's time scale, use mouse wheel scroll on the chart area.
"""

from playwright.sync_api import Page


def _focus_chart(page: Page) -> None:
    """
    Click on the chart canvas to ensure keyboard focus is on the chart,
    not on any toolbar button. This prevents keyboard shortcuts from
    accidentally triggering toolbar buttons (like symbol search).
    """

    try:
        chart_area = page.locator('.layout__area--center')
        if chart_area.count() > 0 and chart_area.first.is_visible():
            chart_area.first.click(position={"x": 400, "y": 300})
            page.wait_for_timeout(300)
            return

        # Fallback: click on a canvas element
        canvas = page.locator("canvas")
        if canvas.count() > 0:
            canvas.first.click()
            page.wait_for_timeout(300)

    except Exception:
        pass


def set_daily_timeframe(page: Page) -> bool:
    """
    Set the TradingView chart timeframe to 1 Day (Daily).

    The correct keyboard sequence is: "1" → "D" → "Enter"
    This opens the timeframe input, types "1D", and confirms it.

    Pressing just "D" alone DOES NOT work — it triggers symbol search.

    Args:
        page: The active Playwright page.

    Returns:
        True if timeframe was set successfully, False otherwise.
    """

    print("[timeframe] Setting timeframe to 1D (Daily)...")

    try:
        # Focus the chart canvas first
        _focus_chart(page)

        # Close any open dialogs
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # Re-focus chart after Escape
        _focus_chart(page)

        # ------------------------------------------------------------------
        # Correct sequence: press "1", then "d", then "Enter"
        # ------------------------------------------------------------------
        # This opens the timeframe input field in the toolbar,
        # types "1D" into it, and confirms the selection.

        page.keyboard.press("1")
        page.wait_for_timeout(300)

        page.keyboard.press("d")
        page.wait_for_timeout(300)

        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)

        print("[timeframe] Timeframe set to Daily (1D).")
        return True

    except Exception as e:
        print(f"[timeframe] ERROR setting timeframe: {e}")
        return False


def zoom_out_chart(page: Page, steps: int = 10) -> None:
    """
    Zoom out the chart to show more candles / wider price history.

    Uses mouse wheel scroll on the chart area. Scrolling DOWN on the
    chart zooms out (shows more candles / compresses the time axis).

    NOTE: Ctrl+Minus and Shift+ArrowLeft zoom the BROWSER, not the chart.
          Mouse wheel on the chart is the correct way to scale the chart.

    Args:
        page:  The active Playwright page.
        steps: Number of scroll steps (default 10). Each step is one
               mouse wheel tick.
    """

    print(f"[timeframe] Zooming out chart with mouse scroll ({steps} steps)...")

    try:
        # Find the chart area to scroll on
        chart_area = page.locator('.layout__area--center')

        if chart_area.count() > 0 and chart_area.first.is_visible():
            # Get the bounding box to find the center of the chart
            box = chart_area.first.bounding_box()

            if box:
                center_x = box["x"] + box["width"] / 2
                center_y = box["y"] + box["height"] / 2

                # Move mouse to the center of the chart
                page.mouse.move(center_x, center_y)
                page.wait_for_timeout(300)

                # Scroll down to zoom out (negative deltaY = zoom in, positive = zoom out)
                # Each scroll step compresses the time axis, showing more candles
                for i in range(steps):
                    page.mouse.wheel(0, 100)  # scroll down = zoom out
                    page.wait_for_timeout(150)

                # Let the chart re-render
                page.wait_for_timeout(1000)

                print("[timeframe] Chart zoomed out.")
            else:
                print("[timeframe] WARNING: Could not get chart bounding box.")
        else:
            print("[timeframe] WARNING: Chart area not found for zoom.")

    except Exception as e:
        print(f"[timeframe] ERROR during zoom: {e}")
