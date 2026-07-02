# PRODUCT.md

# AI-Powered Stock Price Action Analyzer

## Overview

The AI-Powered Stock Price Action Analyzer is an application that allows users to analyze stock charts using computer vision and AI reasoning.

Instead of manually identifying chart patterns, the system generates a candlestick chart from historical market data and passes it to a vision model capable of detecting price action patterns. The detected patterns are then converted into a structured analysis that explains the current market structure.

The objective is **analysis**, not prediction or financial advice.

---

# Problem Statement

Technical traders spend significant time inspecting candlestick charts to identify patterns such as:

* Bullish Engulfing
* Bearish Engulfing
* Hammer
* Shooting Star
* Doji
* Double Top
* Double Bottom
* Head and Shoulders
* Support & Resistance
* Trendlines
* Breakouts

This process is repetitive, subjective, and difficult to automate using traditional rule-based systems.

Recent advances in Vision Language Models make it possible to analyze chart images similarly to how experienced traders visually inspect them.

---

# Product Goal

Build an AI system that can:

1. Accept a stock ticker from the user.
2. Download historical market data.
3. Generate a professional candlestick chart.
4. Analyze the chart using a vision model.
5. Detect technical price action patterns.
6. Generate a structured explanation of the detected market conditions.

---

# Target Users

* Retail traders
* Swing traders
* Students learning technical analysis
* Developers experimenting with AI-powered finance applications
* Researchers exploring computer vision for financial charts

---

# User Journey

1. User enters a stock ticker.
2. System retrieves historical OHLCV data.
3. System generates a candlestick chart.
4. AI analyzes the chart.
5. Detected patterns are summarized.
6. User receives an easy-to-read analysis.

---

# Functional Requirements

The system must:

* Fetch historical stock market data.
* Support ticker-based searches.
* Generate candlestick charts.
* Analyze charts using a vision model.
* Produce structured price action analysis.
* Display detected patterns with confidence scores when available.

---

# Non-Functional Requirements

* Fast response time.
* Modular architecture.
* Easy to extend.
* Easily replaceable AI models.
* Clear separation between components.
* Reproducible outputs where possible.

---

# Success Criteria

The project is considered successful if a user can:

* Enter a stock ticker.
* Receive a generated candlestick chart.
* Obtain an AI-generated explanation of the detected price action.
* Understand the current market structure without manually inspecting the chart.

---

# Version 1 Scope

Version 1 focuses only on historical chart analysis.

Future versions may introduce additional capabilities, but they are intentionally excluded from the initial implementation.
