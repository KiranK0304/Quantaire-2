"""Market data normalization."""

from typing import TYPE_CHECKING

import pandas as pd

from app.exceptions import DataNormalizationError

if TYPE_CHECKING:
    pass


class MarketDataNormalizer:
    """Normalize provider-specific market data into the project's OHLCV schema."""

    REQUIRED_COLUMNS = (
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    )

    def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize raw market data.

        Args:
            data: Raw OHLCV data from a market data provider.

        Returns:
            Normalized OHLCV data.
        """
        data = self._flatten_columns(data)
        self._validate_required_columns(data)
        data = self._drop_incomplete_rows(data)
        data = self._standardize_column_order(data)
        data = self._sort_by_date(data)

        return data

    def _flatten_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Flatten provider-specific MultiIndex columns.

        Args:
            data: Raw provider data.

        Returns:
            DataFrame with one-dimensional column names.
        """
        if isinstance(data.columns, pd.MultiIndex):
            data = data.copy()
            data.columns = data.columns.get_level_values(0)

        return data

    def _validate_required_columns(self, data: pd.DataFrame) -> None:
        """
        Validate that all required OHLCV columns are present.

        Args:
            data: Market data.

        Raises:
            ValueError:
                If one or more required columns are missing.
        """
        missing = set(self.REQUIRED_COLUMNS) - set(data.columns)

        if missing:
            raise DataNormalizationError(
                f"Missing required market data columns: {sorted(missing)}"
            )

    def _drop_incomplete_rows(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Remove incomplete OHLCV rows.

        Args:
            data: Market data.

        Returns:
            Clean market data.
        """
        return data.dropna(subset=self.REQUIRED_COLUMNS)

    def _standardize_column_order(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Reorder columns into the project's OHLCV schema.

        Args:
            data: Market data.

        Returns:
            Ordered market data.
        """
        return data.loc[:, self.REQUIRED_COLUMNS]

    def _sort_by_date(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Ensure market data is ordered chronologically.

        Args:
            data: Market data.

        Returns:
            Chronologically ordered market data.
        """
        return data.sort_index()