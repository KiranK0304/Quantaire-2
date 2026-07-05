"""Pydantic schemas shared across data, chart, vision, and analysis modules."""

from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Period(str, Enum):
    """Supported historical periods."""

    DAY_1 = "1d"
    DAY_5 = "5d"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"
    MONTH_6 = "6mo"
    YEAR_1 = "1y"
    YEAR_2 = "2y"
    YEAR_5 = "5y"


class Interval(str, Enum):
    """Supported market data intervals."""

    MINUTE_1 = "1m"
    MINUTE_2 = "2m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    MINUTE_60 = "60m"
    MINUTE_90 = "90m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    WEEK_1 = "1wk"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"


class MarketDataRequest(BaseModel):
    """Request parameters for historical OHLCV market data retrieval."""

    ticker: str = Field(..., description="Stock ticker symbol to analyze.")
    period: Period = Field(
        default=Period.MONTH_6,
        description="Historical period to retrieve.",
    )
    interval: Interval = Field(
        default=Interval.DAY_1,
        description="Market data interval.",
    )

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        """
        Validate and normalize the ticker symbol.

        Args:
            value: Raw ticker provided by the caller.

        Returns:
            Normalized ticker.
        """
        ticker = value.strip().upper()

        if not ticker:
            raise ValueError("Ticker cannot be empty.")

        return ticker


class ChartArtifact(BaseModel):
    """Metadata describing a generated candlestick chart image."""

    image_path: Path = Field(..., description="Path to the generated chart image.")
    ticker: str = Field(..., description="Ticker represented by the chart.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Chart metadata.")

    def exists(self) -> bool:
        """
        Check whether the chart image artifact exists on disk.

        Returns:
            True when the chart image path exists, otherwise False.
        """
        return self.image_path.exists()


class PatternDetection(BaseModel):
    """Structured representation of a technical pattern detected by vision analysis."""

    name: str = Field(..., description="Detected technical pattern name.")
    confidence: float | None = Field(default=None, description="Optional confidence score.")
    description: str | None = Field(default=None, description="Optional pattern explanation.")
    annotations: dict[str, Any] = Field(default_factory=dict, description="Optional visual annotations.")

    def has_confidence(self) -> bool:
        """
        Check whether the detection includes a confidence score.

        Returns:
            True when confidence is present, otherwise False.
        """
        return self.confidence is not None


class AnalysisReport(BaseModel):
    """Final structured market analysis assembled from detected chart patterns."""

    ticker: str = Field(..., description="Ticker analyzed in the report.")
    summary: str = Field(..., description="Concise market structure summary.")
    detections: list[PatternDetection] = Field(default_factory=list, description="Detected patterns.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional report metadata.")

    def detection_count(self) -> int:
        """
        Count the detected technical patterns in the report.

        Returns:
            Number of pattern detections attached to the report.
        """
        return len(self.detections)

    
class StockInfo(BaseModel):
    """Detailed company and stock information retrieved from Yahoo Finance."""

    # General Info
    long_name: str | None = Field(default=None, description="Full company name.")
    sector: str | None = Field(default=None, description="Company sector.")
    industry: str | None = Field(default=None, description="Company industry.")
    summary: str | None = Field(default=None, description="Long business summary.")
    website: str | None = Field(default=None, description="Company website URL.")
    currency: str | None = Field(default=None, description="Trading currency.")
    
    # Daily Price Action
    previous_close: float | None = Field(default=None, description="Previous day's close price.")
    open_price: float | None = Field(default=None, description="Today's open price.")
    day_low: float | None = Field(default=None, description="Today's low price.")
    day_high: float | None = Field(default=None, description="Today's high price.")
    volume: int | None = Field(default=None, description="Today's trading volume.")
    average_volume: int | None = Field(default=None, description="Average trading volume.")
    
    # Technical & Moving Averages
    fifty_two_week_high: float | None = Field(default=None, description="52-week high price.")
    fifty_two_week_low: float | None = Field(default=None, description="52-week low price.")
    fifty_day_average: float | None = Field(default=None, description="50-day moving average.")
    two_hundred_day_average: float | None = Field(default=None, description="200-day moving average.")
    
    # Valuation & Dividends
    market_cap: int | None = Field(default=None, description="Market capitalization.")
    enterprise_value: int | None = Field(default=None, description="Enterprise value.")
    trailing_pe: float | None = Field(default=None, description="Trailing price-to-earnings ratio.")
    forward_pe: float | None = Field(default=None, description="Forward price-to-earnings ratio.")
    price_to_book: float | None = Field(default=None, description="Price to book ratio.")
    dividend_yield: float | None = Field(default=None, description="Dividend yield percentage.")
    
    # Financial Health & Growth
    profit_margins: float | None = Field(default=None, description="Profit margins.")
    operating_margins: float | None = Field(default=None, description="Operating margins.")
    return_on_equity: float | None = Field(default=None, description="Return on equity.")
    revenue_growth: float | None = Field(default=None, description="Revenue growth.")
    earnings_growth: float | None = Field(default=None, description="Earnings growth.")
    debt_to_equity: float | None = Field(default=None, description="Debt to equity ratio.")
