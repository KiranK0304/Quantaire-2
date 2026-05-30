"""
browser.py — Browser launching and session management.

Handles:
  - Launching Chromium (headless mode configurable)
  - Setting a consistent viewport size for uniform screenshots
  - Navigating to TradingView chart page (not homepage)
  - Waiting for full page load
  - Dismissing ALL popups: login, cookies, ads, upgrade banners, tooltips
  - Providing a persistent browser context for reuse across tickers
"""

from playwright.async_api import async_playwright, Browser, Page, BrowserContext


# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

# Go directly to the CHART page — search/timeframe shortcuts only work here,
# NOT on the in.tradingview.com homepage.
TRADINGVIEW_CHART_URL = "https://in.tradingview.com/chart/"

# Fixed viewport so every screenshot has the same dimensions
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080


async def launch_browser(playwright, headless: bool = True) -> tuple[Browser, BrowserContext, Page]:
    """
    Launch a Chromium browser with a fixed viewport.

    Args:
        playwright: The Playwright instance.
        headless:   Run in headless mode (True) or visible mode (False).

    Returns:
        (browser, context, page) tuple for reuse across the scanning loop.
    """

    mode = "headless" if headless else "visible"
    print(f"[browser] Launching Chromium ({mode} mode)...")

    browser = await playwright.chromium.launch(
        headless=headless,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",  # reduce bot detection
        ],
    )

    # Create a persistent context with a fixed viewport
    context = await browser.new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        # Pretend to be a real user
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    )

    page = await context.new_page()

    return browser, context, page


async def open_tradingview(page: Page) -> None:
    """
    Navigate to TradingView CHART page and wait for it to fully load.
    We go to /chart/ directly because the search and timeframe shortcuts
    only work on the chart page, not the homepage.
    """

    print(f"[browser] Navigating to {TRADINGVIEW_CHART_URL} ...")
    await page.goto(TRADINGVIEW_CHART_URL, wait_until="domcontentloaded")

    # Wait for the chart canvas to appear — this confirms the page is ready
    print("[browser] Waiting for chart to render...")
    try:
        await page.wait_for_selector("canvas", state="visible", timeout=20000)
    except Exception:
        # Sometimes TradingView is slow — reload and try once more
        print("[browser] Chart slow to load, reloading page...")
        await page.reload(wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("canvas", state="visible", timeout=25000)

    # Extra time for the heavy JS app to finish hydrating
    await page.wait_for_timeout(3000)

    # Dismiss any popups that TradingView shows on first visit
    await dismiss_popups(page)

    print("[browser] Chart page loaded.")


async def dismiss_popups(page: Page) -> None:
    """
    Aggressively dismiss ALL types of popups/overlays that TradingView shows.

    TradingView can show any combination of:
      - Login / Sign-in popup (modal asking you to create account)
      - Cookie consent banner
      - Ads / promotional banners
      - "Upgrade to Premium" overlays
      - "Got it!" tooltips (first-visit hints)
      - "Accept cookies" dialogs
      - General close-able modals

    This function tries to dismiss ALL of them without crashing.
    It's safe to call multiple times — it only clicks what's visible.
    """

    print("[popups] Checking for popups to dismiss...")
    dismissed_count = 0

    # ------------------------------------------------------------------
    # 1. "Got it!" tooltips (first-visit feature hints)
    # ------------------------------------------------------------------
    dismissed_count += await _try_click(page, "text=Got it!", "Got it! tooltip")

    # ------------------------------------------------------------------
    # 2. Cookie consent banners
    # ------------------------------------------------------------------
    # Various button texts used for cookie acceptance
    dismissed_count += await _try_click(page, "text=Accept all cookies", "cookie accept (Accept all cookies)")
    dismissed_count += await _try_click(page, "text=Accept All Cookies", "cookie accept (Accept All Cookies)")
    dismissed_count += await _try_click(page, "text=Accept all", "cookie accept (Accept all)")
    dismissed_count += await _try_click(page, "text=I agree", "cookie accept (I agree)")
    dismissed_count += await _try_click(page, "text=Accept", "cookie accept (Accept)")

    # ------------------------------------------------------------------
    # 3. Login / Sign-up popup
    # ------------------------------------------------------------------
    # TradingView shows a login modal that has close buttons.
    # It typically has a title like "Sign in" or "Create account" and
    # an X button to close it.

    # Close button on login modal (usually an SVG X icon)
    dismissed_count += await _try_click(
        page,
        '[data-dialog-name="signup"] button[aria-label="Close"]',
        "signup dialog close"
    )
    dismissed_count += await _try_click(
        page,
        '[data-dialog-name="login"] button[aria-label="Close"]',
        "login dialog close"
    )

    # Generic "No thanks" / "Maybe later" / "Not now" buttons
    dismissed_count += await _try_click(page, "text=No thanks", "No thanks button")
    dismissed_count += await _try_click(page, "text=Maybe later", "Maybe later button")
    dismissed_count += await _try_click(page, "text=Not now", "Not now button")
    dismissed_count += await _try_click(page, "text=No, thanks", "No, thanks button")

    # ------------------------------------------------------------------
    # 4. Upgrade / Premium banners
    # ------------------------------------------------------------------
    dismissed_count += await _try_click(page, "text=Maybe later", "upgrade maybe later")
    dismissed_count += await _try_click(page, "text=Continue with free plan", "continue free plan")
    dismissed_count += await _try_click(page, "text=Stay on Free", "stay on free")

    # ------------------------------------------------------------------
    # 5. Generic close buttons on any visible modal/overlay
    # ------------------------------------------------------------------
    # Try aria-label="Close" buttons (most TradingView modals use this)
    try:
        close_btns = page.locator('[aria-label="Close"]')
        count = await close_btns.count()
        for i in range(count):
            try:
                btn = close_btns.nth(i)
                if await btn.is_visible():
                    await btn.click()
                    dismissed_count += 1
                    print(f"[popups] Dismissed close button #{i+1}.")
                    await page.wait_for_timeout(300)
            except Exception:
                continue
    except Exception:
        pass

    # ------------------------------------------------------------------
    # 6. Overlay/backdrop clicks (close by clicking outside the modal)
    # ------------------------------------------------------------------
    try:
        overlays = page.locator('[class*="overlay"]').or_(
            page.locator('[class*="backdrop"]')
        ).or_(
            page.locator('[class*="dimmer"]')
        )
        if await overlays.count() > 0:
            # Press Escape to close overlays
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)
            dismissed_count += 1
            print("[popups] Pressed Escape to close overlay.")
    except Exception:
        pass

    # ------------------------------------------------------------------
    # 7. Final Escape press to close any remaining dialog
    # ------------------------------------------------------------------
    try:
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
    except Exception:
        pass

    if dismissed_count > 0:
        print(f"[popups] Dismissed {dismissed_count} popup(s).")
    else:
        print("[popups] No popups found.")


async def _try_click(page: Page, selector: str, description: str) -> int:
    """
    Try to find and click an element matching the selector.
    Returns 1 if clicked, 0 if not found or not visible.
    Does NOT raise exceptions.
    """

    try:
        element = page.locator(selector)
        if await element.count() > 0 and await element.first.is_visible():
            await element.first.click()
            print(f"[popups] Dismissed: {description}")
            await page.wait_for_timeout(500)
            return 1
    except Exception:
        pass
    return 0


async def close_browser(browser: Browser) -> None:
    """
    Gracefully close the browser.
    """

    print("[browser] Closing browser...")
    await browser.close()
    print("[browser] Done.")
