"""Pydantic schemas shared across data, chart, vision, and analysis modules."""

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _subtract_months(value: datetime, months: int) -> datetime:
    year = value.year
    month = value.month - months

    while month <= 0:
        month += 12
        year -= 1

    day = min(
        value.day,
        [
            31,
            29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][month - 1],
    )

    return value.replace(year=year, month=month, day=day)


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
    start_date: datetime = Field(
        default_factory=lambda: _subtract_months(_utc_now(), 2),
        description="Start date for historical data retrieval.",
    )
    end_date: datetime = Field(
        default_factory=_utc_now,
        description="End date for historical data retrieval.",
    )
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
