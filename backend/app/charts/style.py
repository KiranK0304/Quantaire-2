"""Chart style configuration for candlestick chart rendering."""


class ChartStyle:
    """Configuration holder for candlestick chart appearance."""

    def __init__(
        self,
        title: str | None = None,
        volume: bool = True,
        style_name: str = "yahoo",
    ) -> None:
        """
        Create chart style settings.

        Args:
            title: Optional chart title.
            volume: Whether to include a volume panel.
            style_name: mplfinance style name.
        """
        self.title = title
        self.volume = volume
        self.style_name = style_name

    def to_mplfinance_kwargs(self) -> dict[str, object]:
        """
        Convert chart style settings into mplfinance keyword arguments.

        Returns:
            Keyword arguments for chart rendering.
        """
        return {
            "type": "candle",
            "style": self.style_name,
            "volume": self.volume,
            "figratio": (16, 9),
            "figscale": 1.2,
            "ylabel": "Price",  
            "ylabel_lower": "Volume",
            "tight_layout": True,
        }
