"""Market data normalization skeletons."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


class MarketDataNormalizer:
    """Normalize provider-specific market data into the project OHLCV schema."""

    def __init__(self, required_columns: tuple[str, ...] | None = None) -> None:
        """
        Create a market data normalizer.

        Args:
            required_columns: Optional required OHLCV column names.
        """
        self.required_columns = required_columns or ("Open", "High", "Low", "Close", "Volume")

    def normalize(self, data: "pd.DataFrame") -> "pd.DataFrame":
        """
        Normalize raw market data.

        Args:
            data: Raw OHLCV data from a market data provider.

        Returns:
            Clean OHLCV data using the expected project schema.
        """
        # TODO: Receive raw data from MarketDataFetcher.fetch().
        # TODO: Call self._validate_required_columns(data) before transformations.
        # TODO: Call self._drop_incomplete_rows(data) to remove unusable rows.
        # TODO: Call self._standardize_column_order(data) to produce the expected schema.
        # TODO: Return normalized data to CandlestickChartGenerator.generate_chart().
        pass

    def _validate_required_columns(self, data: "pd.DataFrame") -> None:
        """
        Validate that all required OHLCV columns are present.

        Args:
            data: Raw or partially normalized market data.

        Returns:
            None.
        """
        # TODO: Compare data columns with self.required_columns.
        # TODO: Raise a validation error when required OHLCV columns are missing.
        pass

    def _drop_incomplete_rows(self, data: "pd.DataFrame") -> "pd.DataFrame":
        """
        Remove rows that cannot be used for chart generation.

        Args:
            data: Market data that may contain incomplete OHLCV rows.

        Returns:
            Market data with incomplete rows removed.
        """
        # TODO: Remove rows with missing OHLCV values.
        # TODO: Return cleaned data to normalize().
        pass

    def _standardize_column_order(self, data: "pd.DataFrame") -> "pd.DataFrame":
        """
        Reorder market data columns into the project OHLCV schema.

        Args:
            data: Validated market data.

        Returns:
            Market data using the configured required column order.
        """
        # TODO: Select columns using self.required_columns.
        # TODO: Return ordered data to normalize().
        pass
