"""Historical market data retrieval."""

import yfinance as yf
from typing import TYPE_CHECKING

from app.schemas import MarketDataRequest

if TYPE_CHECKING:
    import pandas as pd


class MarketDataFetcher:
    """Fetch historical OHLCV data from the configured market data provider."""

    def __init__(self) -> None:
        """
        Create a market data fetcher.
        """
        pass

    def fetch(self, request: MarketDataRequest) -> "pd.DataFrame":
        """
        Fetch historical market data.

        Args:
            request: Validated market data request.

        Returns:
            Raw historical OHLCV data from the provider.
        """
        return self._download_market_data(
            ticker=request.ticker,
            period=request.period.value,
            interval=request.interval.value,
        )

    def _download_market_data(
        self,
        ticker: str,
        period: str,
        interval: str,
    ) -> "pd.DataFrame":
        """
        Download historical market data from the configured provider.

        Args:
            ticker: Validated ticker symbol.
            period: Historical data period.
            interval: Historical data interval.

        Returns:
            Provider-specific OHLCV data as a pandas DataFrame.

        Raises:
            ValueError:
                If no market data is returned.
        """
        data = yf.download(
            tickers=ticker,
            interval=interval,
            progress=False,
            auto_adjust=False,
            period=period,
        )

        if data.empty:
            raise ValueError(f"No market data found for ticker '{ticker}'.")

        return data