"""Application configuration skeletons."""

from pathlib import Path

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration separated from business logic."""

    chart_output_dir: Path = Field(default=Path("outputs/charts"), description="Chart output directory.")
    default_period: str = Field(default="6mo", description="Default historical data period.")
    default_interval: str = Field(default="1d", description="Default historical data interval.")
    vision_model_name: str | None = Field(default=None, description="Optional vision model identifier.")

    def chart_path_for_ticker(self, ticker: str) -> Path:
        """
        Build the expected chart image path for a ticker.

        Args:
            ticker: Ticker represented by the generated chart.

        Returns:
            Path where the ticker chart should be written.
        """
        # TODO: Receive ticker from main.analyze_ticker().
        # TODO: Combine self.chart_output_dir with a deterministic ticker filename.
        # TODO: Return chart path to PriceActionAnalysisService.analyze_ticker().
        pass
