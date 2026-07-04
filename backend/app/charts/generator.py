"""Candlestick chart generation."""

from pathlib import Path
from typing import TYPE_CHECKING, Any
import mplfinance as mpf


from app.charts.style import ChartStyle
from app.schemas import ChartArtifact

if TYPE_CHECKING:
    import pandas as pd


class CandlestickChartGenerator:
    """Generate candlestick chart images from normalized OHLCV data."""

    REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Volume")

    def __init__(self, style: ChartStyle | None = None) -> None:
        """
        Create a candlestick chart generator.

        Args:
            style: Optional chart style configuration.
        """
        self.style = style or ChartStyle()

    def generate_chart(
        self,
        data: "pd.DataFrame",
        ticker: str,
        output_path: Path,
    ) -> ChartArtifact:
        """
        Generate a candlestick chart image from OHLCV data.

        Args:
            data: Normalized market data.
            ticker: Ticker represented by the chart.
            output_path: Location where the chart image will be saved.

        Returns:
            Metadata for the generated chart image.
        """
        self._validate_market_data(data)

        chart_title = self.style.title or self._build_chart_title(ticker)
        image_path = self._render_chart(
            data=data,
            output_path=output_path,
            chart_title=chart_title,
        )

        return ChartArtifact(
            image_path=image_path,
            ticker=ticker,
            metadata={
                "title": chart_title,
                "style": self.style.style_name,
                "volume": self.style.volume,
                "rows": len(data),
            },
        )

    def _render_chart(
        self,
        data: "pd.DataFrame",
        output_path: Path,
        chart_title: str,
    ) -> Path:
        """
        Render a candlestick chart image to disk.

        Args:
            data: Normalized OHLCV data.
            output_path: Destination path for the chart image.
            chart_title: Title to display on the chart.

        Returns:
            Path to the rendered chart image.
        """

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        chart_options: dict[str, Any] = self.style.to_mplfinance_kwargs()
        chart_options["title"] = chart_title
        chart_options["savefig"] = {
            "fname": output_path,
            "dpi": 150,
            "bbox_inches": "tight",
        }

        mpf.plot(data, **chart_options)

        return output_path

    def _build_chart_title(self, ticker: str) -> str:
        """
        Build a chart title for a ticker.

        Args:
            ticker: Stock ticker displayed in the chart title.

        Returns:
            Chart title text.
        """
        return f"{ticker.upper()} Price Action"

    def _validate_market_data(self, data: "pd.DataFrame") -> None:
        """
        Validate normalized market data before rendering.

        Args:
            data: Normalized OHLCV data.

        Returns:
            None.

        Raises:
            ValueError:
                If the market data cannot be rendered as a candlestick chart.
        """
        if data.empty:
            raise ValueError("Cannot generate chart from empty market data.")

        try:
            import pandas as pd
        except ImportError as exc:
            raise RuntimeError(
                "pandas is required to validate and generate candlestick charts."
            ) from exc

        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Market data index must be a pandas DatetimeIndex.")

        missing_columns = set(self.REQUIRED_COLUMNS) - set(data.columns)
        if missing_columns:
            raise ValueError(
                f"Missing required chart columns: {sorted(missing_columns)}"
            )

        if data.index.hasnans:
            raise ValueError("Market data index cannot contain missing dates.")
