"""Custom exceptions for the Price Action Analyzer application."""


class PriceActionAnalyzerError(Exception):
    """Base exception for all application-specific errors."""

    def __init__(self, message: str):
        super().__init__(message)


class MarketDataNotFoundError(PriceActionAnalyzerError):
    """Raised when no market data is available for the requested ticker."""

    def __init__(self, ticker: str):
        super().__init__(
            f"No market data found for ticker '{ticker}'."
        )


class DataNormalizationError(PriceActionAnalyzerError):
    """Raised when market data cannot be normalized."""

    def __init__(self, reason: str):
        super().__init__(
            f"Failed to normalize market data: {reason}"
        )


class ChartGenerationError(PriceActionAnalyzerError):
    """Raised when candlestick chart generation fails."""

    def __init__(self, ticker: str):
        super().__init__(
            f"Failed to generate candlestick chart for '{ticker}'."
        )


class VisionInferenceError(PriceActionAnalyzerError):
    """Raised when the vision model fails to analyze the chart."""

    def __init__(self, reason: str):
        super().__init__(
            f"Vision inference failed: {reason}"
        )