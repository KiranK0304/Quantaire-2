# Quantaire-2: Stock Market Pattern Detection

An automated, computer-vision based pipeline that captures real-time stock charts from TradingView and uses a custom-trained **YOLOv8** object detection model to identify technical chart patterns (e.g., Head and Shoulders, Double Bottoms, Triangles).

## 🚀 Features

- **Headless TradingView Automation:** Uses Playwright to navigate TradingView, search for tickers, set timeframes (Daily), zoom, and capture clean chart screenshots.
- **Anti-Blocking Robustness:** Implements auto-retry logic with fresh incognito sessions to bypass TradingView's aggressive signup overlays and rate limits during batch scanning.
- **YOLOv8 Inference:** Detects multiple technical patterns simultaneously using a custom `.pt` model.
- **In-Memory Single Stock Analysis:** Analyze any stock on-demand without writing intermediate screenshots to disk.
- **Automated Logging:** Generates structured JSON logs for both scanner success/failure rates and detection results.

---

## 📂 Project Structure

```text
pattern_detections/
│
├── configs/                  # Global settings, paths, and configurations
├── detector/                 # YOLO model loading, inference, and OpenCV visualization
├── pipeline/                 
│   ├── main.py               # Entry point for batch scanning and detection
│   └── analyze.py            # Entry point for single-stock in-memory analysis
├── tradingview/              # Playwright browser automation (search, capture, timeframe)
│
├── screenshots/              # Raw captured charts from the batch scanner
│   └── analyzed/             # Annotated outputs from single-stock analysis
├── outputs/
│   ├── annotated/            # Annotated outputs from batch detection
│   └── logs/                 # JSON logs for scanner runs and detection results
│
└── stockmarket-pattern-detection-yolov8/
    └── model.pt              # The trained YOLOv8 weights
```

---

## 🛠️ Setup & Installation

This project uses `uv` for fast dependency management.

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Install Playwright browsers:**
   ```bash
   uv run playwright install chromium
   ```

---

## 💻 Usage

### 1. Full Batch Pipeline (Scan + Detect)
Automatically loops through a predefined list of stocks, captures their charts from TradingView, and runs the YOLO detection model on all of them.
```bash
uv run python -m pipeline.main --with-scanner
```
- Raw screenshots are saved to `screenshots/`
- Annotated images are saved to `outputs/annotated/`
- Run logs are saved to `outputs/logs/`

### 2. Run Detection Only
If you already have screenshots in the `screenshots/` folder and only want to run the YOLO model over them:
```bash
uv run python -m pipeline.main
```

### 3. Single Stock Analysis (In-Memory)
Search and analyze a specific stock instantly. The chart is captured directly into memory (no raw disk writes) and fed to the YOLO model.
```bash
# Basic run
uv run python -m pipeline.analyze HDFCBANK

# Run with visual preview (pops up a matplotlib window of the chart before inference)
uv run python -m pipeline.analyze HDFCBANK --show
```
- Annotated output is saved to `screenshots/analyzed/HDFCBANK_detected.png`
