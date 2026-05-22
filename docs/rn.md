Ran command: `python run_scanner.py`
Ran command: `uv run run_scanner.py`
Viewed run_scanner.py:1-27
Ran command: `cd ..`
Ran command: `uv run tradingview/run_scanner.py`
Ran command: `cd ..`

Run it from the **project root** using the `-m` flag:

```bash
cd /home/Kiran/work/market_projects/pattern_detections
uv run python -m tradingview.run_scanner
```

The `-m` flag tells Python to treat `tradingview` as a package and adds the current directory to `sys.path`. That's why the imports use `from tradingview.browser import ...`.

**Why the other attempts failed:**
- `python run_scanner.py` from inside `tradingview/` — wrong Python (system, no playwright installed) + no parent package context
- `uv run run_scanner.py` — runs the file directly, doesn't set up the package path
- `uv run tradingview/run_scanner.py` — same problem, runs as a script not a module