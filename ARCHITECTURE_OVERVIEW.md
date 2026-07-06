# Price Action Analyzer - Architecture & Project Overview

## 1. Project Purpose
The **Price Action Analyzer** is a full-stack web application designed to automatically detect technical chart patterns in financial markets. It fetches historical OHLCV (Open, High, Low, Close, Volume) data for a requested stock ticker, generates a high-resolution candlestick chart, runs a custom-trained computer vision model (YOLO) over the chart to find technical patterns, and returns an annotated chart alongside comprehensive stock metadata.

## 2. Technology Stack
**Backend:**
*   **Framework:** FastAPI (Python 3.11)
*   **Data Fetching:** `yfinance` (Historical market data and fundamental stock metrics)
*   **Charting Engine:** `mplfinance` backed by `matplotlib` (using the non-interactive `Agg` backend to ensure thread-safety in an asynchronous web environment)
*   **Computer Vision:** `ultralytics` (YOLO) for object detection. OpenCV (`cv2`) for custom drawing of high-visibility neon green bounding boxes over the charts.

**Frontend:**
*   **Framework:** React 18 with TypeScript, bundled via Vite.
*   **Styling:** Pure Vanilla CSS (`index.css`) built around a highly responsive, premium "trading terminal" aesthetic (dark mode, monospaced fonts, rounded data modules, low-contrast grays for readability, neon green accents).
*   **State Management:** React Hooks (`useState`, `useEffect`) fetching data in parallel via standard browser `fetch` API.

## 3. Core Workflow
1.  **Request Initiation:** The user inputs a ticker (e.g., `TCS.NS`, `AAPL`) and selects a market region via the frontend.
2.  **Parallel Fetching (`Analysis.tsx`):** The frontend fires two requests simultaneously:
    *   `POST /analyze`: Triggers the heavy chart generation and vision inference pipeline.
    *   `GET /info/{ticker}`: Instantly fetches fundamental metadata (Market Cap, P/E ratio, etc.).
3.  **Backend Pipeline (`api/routers/analysis.py`):**
    *   **Data Layer:** Retrieves 6 months of daily OHLCV data.
    *   **Chart Layer:** Plots a dark-themed candlestick chart and saves it as a temporary artifact on disk.
    *   **Vision Layer:** Loads the generated chart image, runs the YOLO model to detect technical patterns (like `W_Bottom`, `M_Head`, `Head and shoulders top`, etc.), and uses OpenCV to draw boxes over the coordinates.
4.  **Response Handling:** The API returns a unified `AnalysisReport` JSON containing pattern names, confidence scores, and detection counts.
5.  **UI Rendering:** The React app dynamically builds a single-column, scroll-friendly dashboard containing the annotated chart, a clean scan summary, individual detection cards, and a fundamental `StockMetrics` dashboard.

## 4. Key Schemas & Data Structures
Located in `backend/app/schemas/schemas.py`, the core models include:
*   `StockInfo`: Comprehensive fundamental metrics (Price action, Technical Averages, Valuations, Financial Health, Business Summary).
*   `PatternDetection`: Schema for a single model detection (Name, Confidence, Bounding Box coordinates).
*   `AnalysisReport`: The final payload returned to the frontend.

## 5. Current State of the Project
*   **Backend:** Fully stable. The endpoints (`/analyze`, `/chart/{ticker}`, `/info/{ticker}`) are wired and working. Thread-safety issues regarding matplotlib GUI execution have been permanently resolved.
*   **Frontend:** The UI is complete, highly polished, and fully responsive across mobile and desktop. Advanced UX features (like modal pop-ups for long business summaries, and conditional CTA buttons) are implemented.
*   **Next Steps for Future Agents:** The architecture is modular, meaning future AI agents can easily plug in new features such as: 
    *   Swapping the local YOLO model for a different inference engine.
    *   Adding more technical indicators (RSI, MACD) to the backend data fetcher.
    *   Implementing a database layer (e.g., PostgreSQL or SQLite) if you want to store historical analysis scans.
