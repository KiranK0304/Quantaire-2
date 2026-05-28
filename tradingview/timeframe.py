"""
timeframe.py — Timeframe selection logic.

Handles setting the chart timeframe, date range, and zoom.
"""

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from playwright.sync_api import Page


RANGE_OFFSETS = {
    "1M": relativedelta(months=1),
    "3M": relativedelta(months=3),
    "6M": relativedelta(months=6),
    "1Y": relativedelta(years=1),
}


def _focus_chart(page: Page) -> None:
    """Focus the chart canvas to prevent accidental toolbar shortcuts."""

    try:
        chart_area = page.locator('.layout__area--center')
        if chart_area.count() > 0 and chart_area.first.is_visible():
            chart_area.first.click(position={"x": 400, "y": 300})
            page.wait_for_timeout(300)
            return

        canvas = page.locator("canvas")
        if canvas.count() > 0:
            canvas.first.click()
            page.wait_for_timeout(300)

    except Exception:
        pass


def set_timeframe(page: Page, tf: str) -> bool:
    """Set the TradingView chart timeframe dynamically (e.g., '1D', '1W', '1h')."""
    print(f"[timeframe] Setting timeframe to {tf}...")

    try:
        _focus_chart(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        _focus_chart(page)

        for char in tf:
            page.keyboard.press(char)
            page.wait_for_timeout(300)

        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)

        print(f"[timeframe] Timeframe set to {tf}.")
        return True

    except Exception as e:
        print(f"[timeframe] ERROR setting timeframe: {e}")
        return False


def set_date_range(page: Page, date_range: str) -> bool:
    """
    Set the chart's visible date range using Alt+G 'Go to' → 'Custom range'.
    Calculates start/end dates dynamically (e.g. '3M' = 3 months ago → today).
    """
    date_range = date_range.upper()
    offset = RANGE_OFFSETS.get(date_range)

    if not offset:
        print(f"[timeframe] ERROR: Unsupported date range '{date_range}'")
        return False

    today = date.today()
    start_date = today - offset
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = today.strftime("%Y-%m-%d")

    print(f"[timeframe] Setting custom range: {start_str} → {end_str} ({date_range})...")

    try:
        # 1. Focus chart and open Go-to dialog with Alt+G
        _focus_chart(page)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        _focus_chart(page)
        page.keyboard.press("Alt+g")
        page.wait_for_timeout(1000)

        # 2. Click the "Custom range" tab
        custom_tab = page.get_by_text("Custom range", exact=True)
        if custom_tab.count() > 0:
            custom_tab.first.click()
            page.wait_for_timeout(500)
        else:
            print("[timeframe] WARNING: 'Custom range' tab not found, trying to proceed...")

        # 3. Find date inputs (skip disabled time inputs)
        # Dialog layout: [start_date, start_time(disabled), end_date, end_time(disabled)]
        all_inputs = page.locator('[class*="dialog"] input').all()
        print(f"[timeframe] Dialog inputs found: {len(all_inputs)}")

        # Filter to only enabled date inputs (not the disabled time pickers)
        date_inputs = []
        for inp in all_inputs:
            is_disabled = inp.get_attribute("disabled") is not None
            qa_id = inp.get_attribute("data-qa-id") or ""
            if not is_disabled and "time-input" not in qa_id:
                date_inputs.append(inp)

        print(f"[timeframe] Usable date inputs: {len(date_inputs)}")

        if len(date_inputs) >= 2:
            # Clear and fill start date
            date_inputs[0].click(click_count=3)
            page.wait_for_timeout(200)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            date_inputs[0].type(start_str, delay=50)
            page.wait_for_timeout(300)

            # Clear and fill end date
            date_inputs[1].click(click_count=3)
            page.wait_for_timeout(200)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            date_inputs[1].type(end_str, delay=50)
            page.wait_for_timeout(300)
            
            # Press Enter to submit the dialog
            page.keyboard.press("Enter")
        elif len(all_inputs) >= 3:
            # Fallback: use indices 0 (start date) and 2 (end date)
            print("[timeframe] Using fallback indices 0 and 2...")
            all_inputs[0].click(click_count=3)
            page.wait_for_timeout(200)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            all_inputs[0].type(start_str, delay=50)
            page.wait_for_timeout(300)
            
            all_inputs[2].click(click_count=3)
            page.wait_for_timeout(200)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(200)
            all_inputs[2].type(end_str, delay=50)
            page.wait_for_timeout(300)
            
            page.keyboard.press("Enter")
        else:
            print("[timeframe] ERROR: Could not find enough date inputs in dialog.")
            page.keyboard.press("Escape")
            return False

        # Wait for chart to re-render
        page.wait_for_timeout(2500)

        print(f"[timeframe] Date range set to {date_range} ({start_str} → {end_str}).")
        return True

    except Exception as e:
        print(f"[timeframe] ERROR setting date range: {e}")
        # Try to close dialog if it's still open
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass
        return False


def zoom_out_chart(page: Page, steps: int = 10) -> None:
    """Zoom out the chart to show more candles using mouse scroll."""

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
