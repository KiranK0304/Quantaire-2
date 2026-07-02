"""Pydantic schemas shared across data, chart, vision, and analysis modules."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class MarketDataRequest(BaseModel):
    """Request parameters for historical OHLCV market data retrieval."""

    ticker: str = Field(..., description="Stock ticker symbol to analyze.")
    period: str = Field(default="6mo", description="Historical period to retrieve.")
    interval: str = Field(default="1d", description="Market data interval.")

    def normalized_ticker(self) -> str:
        """
        Return a normalized ticker symbol for downstream services.

        Returns:
            Normalized ticker symbol.
        """
        # TODO: Strip surrounding whitespace from self.ticker.
        # TODO: Convert the ticker into the canonical provider format.
        # TODO: Return the normalized ticker to MarketDataFetcher.fetch().
        pass


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
        # TODO: Check self.image_path after CandlestickChartGenerator.generate_chart() writes it.
        # TODO: Return the existence result to workflow validation code.
        pass


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
        # TODO: Inspect self.confidence after PatternDetector parses model output.
        # TODO: Return whether confidence can be displayed in the final report.
        pass


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
        # TODO: Count self.detections after AnalysisEngine.generate_report() builds the report.
        # TODO: Return the count for UI or API presentation code.
        pass
