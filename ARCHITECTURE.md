# ARCHITECTURE.md

# System Architecture

## Core Objective

Build a modular AI-powered stock chart analysis system that converts historical market data into a candlestick chart and uses a vision model to detect technical price action patterns.

The system should produce structured market analysis while remaining simple, maintainable, and easy to extend.

---

# Scope Definition

## Core Loop

```
User enters stock ticker
        ↓
Fetch historical market data
        ↓
Generate candlestick chart
        ↓
Analyze chart using Vision AI
        ↓
Extract detected price action
        ↓
Generate structured analysis
        ↓
Display results
```

---

## In Scope

* Historical stock data retrieval
* Candlestick chart generation
* Vision-based chart analysis
* Pattern detection
* Structured AI explanations
* Modular Python implementation

---

## Out of Scope

The system will NOT:

* Execute trades
* Connect to brokerage accounts
* Manage portfolios
* Predict future prices
* Perform algorithmic trading
* Stream real-time market data
* Support options or futures analysis
* Provide financial advice
* Implement authentication or user accounts
* Include a mobile application

These features may be considered in future versions but are intentionally excluded from Version 1.

---

# Technology Stack

## Language

* Python 3.11+

## Core Libraries

* pandas
* numpy
* yfinance (initial implementation)
* mplfinance
* matplotlib
* OpenCV
* Pydantic
* FastAPI (future API layer)
* PyTorch
* Transformers

---

# Project Structure

```
project/

│
├── docs/
│   ├── PRODUCT.md
│   └── ARCHITECTURE.md
│
├── app/
│   ├── data/
│   ├── charts/
│   ├── vision/
│   ├── analysis/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── config/
│
├── tests/
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# Module Responsibilities

## Data Module

Responsibilities

* Download historical OHLCV data
* Validate ticker input
* Normalize market data

Outputs

* Clean pandas DataFrame

---

## Chart Module

Responsibilities

* Generate candlestick charts
* Configure chart appearance
* Export chart image

Outputs

* PNG chart image

---

## Vision Module

Responsibilities

* Analyze chart images
* Detect technical patterns
* Return structured findings

Outputs

* Pattern detections
* Confidence scores
* Optional annotations

---

## Analysis Module

Responsibilities

* Interpret detected patterns
* Generate structured market summary
* Combine findings into a single report

Outputs

* Analysis object

---

# Data Flow

```
Ticker
    ↓
Data Fetcher
    ↓
OHLCV DataFrame
    ↓
Chart Generator
    ↓
Chart Image
    ↓
Vision Model
    ↓
Detected Patterns
    ↓
Analysis Engine
    ↓
Final Report
```

---

# Coding Standards

* Use Python type hints for all public functions.
* Prefer small, single-purpose modules.
* Keep functions focused on one responsibility.
* Use descriptive variable names.
* Validate external inputs.
* Avoid unnecessary abstraction.
* Write concise docstrings.
* Use logging instead of print statements.
* Store configuration separately from business logic.

---

# Design Principles

* Modular architecture
* Clear separation of concerns
* Deterministic data flow
* Replaceable AI models
* Minimal dependencies between modules
* Easy testing and maintenance

---

# AI Development Rules

When modifying this project:

* Do not create files outside the defined directory structure.
* Do not introduce new dependencies without approval.
* Reuse existing modules before creating new ones.
* Keep interfaces stable unless explicitly instructed.
* Return structured data instead of formatted text whenever possible.
* Never hardcode API keys or secrets.
* Do not add features that are outside the defined project scope.
* Prioritize readability over cleverness.

---

# Future Extensions

Potential future enhancements include:

* Multi-timeframe analysis
* Real-time market data
* Multiple vision models
* News integration
* Retrieval-Augmented Generation (RAG)
* Multi-agent reasoning
* Portfolio analysis
* Broker integration
* Web dashboard
* Mobile application

These are intentionally excluded from Version 1.
