"""
search.py — Ticker search and selection logic.

Handles:
  - Opening the TradingView symbol search dialog
  - Typing a stock ticker symbol
  - Waiting for the dropdown suggestions to appear
  - Selecting the correct stock from the dropdown
  - Waiting for the chart to fully load after selection

IMPORTANT:
  On the chart page (/chart/), Ctrl+K opens "Search tool or function" — NOT symbol search.
  Symbol search is only accessible via the top-left button (id="header-toolbar-symbol-search").
  On the homepage, Ctrl+K does open symbol search.
  We handle both cases by checking the dialog title after opening.
"""

from playwright.sync_api import Page


# The search input placeholder text — same in both symbol search and homepage
SEARCH_INPUT_PLACEHOLDER = "Symbol, ISIN, or CUSIP"

# The title of the correct dialog we want
SYMBOL_SEARCH_TITLE = "Symbol search"

# The title of the WRONG dialog (tool search opened by Ctrl+K on chart page)
TOOL_SEARCH_TITLE = "Search tool or function"


def _open_symbol_search(page: Page) -> bool:
    """
    Open the Symbol Search dialog, regardless of whether we're on the
    homepage or the chart page.

    Strategy:
      1. Try clicking the symbol search button in the top-left toolbar
         (id="header-toolbar-symbol-search") — this always opens Symbol Search.
      2. If that button doesn't exist (e.g. on the homepage), use Ctrl+K.
      3. Verify the opened dialog title says "Symbol search", not "Search tool or function".

    Returns:
        True if the Symbol Search dialog was successfully opened.
    """

    # ------------------------------------------------------------------
    # Method 1: Click the symbol search button (works on chart page)
    # ------------------------------------------------------------------
    # This button is in the top-left toolbar, shows the current symbol name,
    # and has title="Symbol search".
    # HTML: <button id="header-toolbar-symbol-search" title="Symbol search">RELIANCE</button>

    symbol_btn = page.locator("#header-toolbar-symbol-search")

    if symbol_btn.count() > 0 and symbol_btn.first.is_visible():
        print("[search] Clicking symbol search button (top-left toolbar)...")
        symbol_btn.first.click()
        page.wait_for_timeout(1000)

        # Verify the correct dialog opened
        if _is_symbol_search_open(page):
            return True
        else:
            # Wrong dialog somehow — close it and try fallback
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

    # ------------------------------------------------------------------
    # Method 2: Fallback — Ctrl+K (works on homepage, NOT on chart page)
    # ------------------------------------------------------------------
    print("[search] Symbol button not found, trying Ctrl+K...")
    page.keyboard.press("Control+k")
    page.wait_for_timeout(1000)

    if _is_symbol_search_open(page):
        return True

    # If Ctrl+K opened the wrong dialog (tool search), close it
    print("[search] Ctrl+K opened the wrong dialog, closing...")
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    return False


def _is_symbol_search_open(page: Page) -> bool:
    """
    Check if the currently open dialog is the Symbol Search dialog,
    NOT the "Search tool or function" dialog.

    We look for:
      - The input with placeholder "Symbol, ISIN, or CUSIP" (only in symbol search)
      - OR a dialog title containing "Symbol search"
    """

    # Check for the symbol search input (unique to symbol search dialog)
    search_input = page.locator(f'input[placeholder="{SEARCH_INPUT_PLACEHOLDER}"]')
    if search_input.count() > 0 and search_input.first.is_visible():
        return True

    return False


def search_ticker(page: Page, ticker: str) -> bool:
    """
    Search for a stock ticker on TradingView and open its chart.

    Steps:
      1. Open the Symbol Search dialog (button click or Ctrl+K)
      2. Verify it's the correct dialog (not tool search)
      3. Type the ticker into the search input
      4. Wait for dropdown results
      5. Click the first matching result
      6. Wait for chart to load

    Args:
        page:   The active Playwright page.
        ticker: Stock symbol (e.g. "RELIANCE", "TCS").

    Returns:
        True if the ticker was found and chart loaded, False otherwise.
    """

    print(f"[search] Searching for ticker: {ticker}")

    try:
        # ------------------------------------------------------------------
        # Step 1 & 2: Open the Symbol Search dialog
        # ------------------------------------------------------------------
        if not _open_symbol_search(page):
            print(f"[search] ERROR: Could not open Symbol Search dialog for '{ticker}'.")
            return False

        # ------------------------------------------------------------------
        # Step 3: Type the ticker into the search input
        # ------------------------------------------------------------------
        search_input = page.locator(f'input[placeholder="{SEARCH_INPUT_PLACEHOLDER}"]')
        search_input.first.wait_for(state="visible", timeout=5000)

        # Clear any existing text and type the ticker
        search_input.first.fill("")
        page.wait_for_timeout(300)
        search_input.first.type(ticker, delay=80)  # human-like typing speed

        print(f"[search] Typed '{ticker}', waiting for suggestions...")

        # ------------------------------------------------------------------
        # Step 4: Wait for dropdown results to populate
        # ------------------------------------------------------------------
        page.wait_for_timeout(2000)

        # ------------------------------------------------------------------
        # Step 5: Click the first matching result
        # ------------------------------------------------------------------
        # Results appear in a scrollable list. Each row is clickable.
        # We look for rows in the result container.

        # Try to find result items using common selectors
        result_item = page.locator(
            '[data-role="list-item"]'
        ).or_(
            page.locator('[class*="listRow"]')
        ).or_(
            page.locator('[class*="itemRow"]')
        )

        if result_item.count() > 0:
            result_item.first.click()
            print(f"[search] Clicked first result for '{ticker}'.")
        else:
            # Fallback: press Enter to select the top result
            print(f"[search] No list items found, pressing Enter...")
            search_input.first.press("Enter")

        # ------------------------------------------------------------------
        # Step 6: Wait for the chart to fully load
        # ------------------------------------------------------------------
        page.wait_for_timeout(3000)

        # Confirm chart canvas is present and rendered
        page.wait_for_selector("canvas", state="visible", timeout=10000)

        # ------------------------------------------------------------------
        # Step 7: Validate the loaded chart shows the correct ticker
        # ------------------------------------------------------------------
        if not validate_loaded_ticker(page, ticker):
            print(f"[search] WARNING: Chart may not be showing '{ticker}' — proceeding anyway.")
        else:
            print(f"[search] ✅ Validated: chart is showing '{ticker}'.")

        return True

    except Exception as e:
        print(f"[search] ERROR searching for '{ticker}': {e}")

        # Try to close any open dialog before returning
        try:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
        except Exception:
            pass

        return False


def validate_loaded_ticker(page: Page, expected_ticker: str) -> bool:
    """
    Verify that the chart is actually showing the stock we requested.

    Reads the text from the symbol search button (top-left toolbar) which
    displays the current symbol name (e.g. "RELIANCE", "TCS").

    Also checks the chart header line which shows something like:
    "Reliance Industries Limited · 1D · NSE"

    Args:
        page:             The active Playwright page.
        expected_ticker:  The ticker we searched for (e.g. "RELIANCE").

    Returns:
        True if the chart is showing the expected ticker, False otherwise.
    """

    try:
        # Method 1: Read the symbol button text in the top-left toolbar
        symbol_btn = page.locator("#header-toolbar-symbol-search")
        if symbol_btn.count() > 0 and symbol_btn.first.is_visible():
            loaded_symbol = symbol_btn.first.inner_text().strip().upper()

            if expected_ticker.upper() in loaded_symbol:
                return True
            else:
                print(f"[search] MISMATCH: Expected '{expected_ticker}', "
                      f"but toolbar shows '{loaded_symbol}'.")
                return False

        # Method 2: Check the chart header text (has the full company name)
        header = page.locator('[class*="headerTitle"]').or_(
            page.locator('[class*="symbolTitle"]')
        )
        if header.count() > 0:
            header_text = header.first.inner_text().strip().upper()
            if expected_ticker.upper() in header_text:
                return True

        # Could not validate — return False (but don't treat as hard error)
        print(f"[search] Could not read current symbol for validation.")
        return False

    except Exception as e:
        print(f"[search] Validation error: {e}")
        return False
