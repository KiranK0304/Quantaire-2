"""Historical market data retrieval skeletons."""

from typing import TYPE_CHECKING

from app.data.validator import TickerValidator
from app.models import MarketDataRequest

if TYPE_CHECKING:
    import pandas as pd


class MarketDataFetcher:
    """Fetch historical OHLCV data from the configured market data provider."""

    def __init__(self, validator: TickerValidator | None = None) -> None:
        """
        Create a market data fetcher.

        Args:
            validator: Optional ticker validator used before data retrieval.
        """
        self.validator = validator or TickerValidator()

    def fetch(self, request: MarketDataRequest) -> "pd.DataFrame":
        """
        Fetch historical market data for a ticker.

        Args:
            request: Market data request parameters.

        Returns:
            Historical OHLCV data as a pandas DataFrame.
        """
        # TODO: Call request.normalized_ticker() to prepare the provider symbol.
        # TODO: Pass the normalized ticker into self.validator.validate().
        # TODO: Call self._download_from_provider(validated_ticker, request.period, request.interval).
        # TODO: Return raw OHLCV data to PriceActionAnalysisService.analyze_ticker().
        pass

    def _download_from_provider(
        self,
        ticker: str,
        period: str,
        interval: str,
    ) -> "pd.DataFrame":
        """
        Download historical OHLCV data from the market data provider.

        Args:
            ticker: Validated ticker symbol.
            period: Historical period requested.
            interval: Historical data interval requested.

        Returns:
            Provider-specific raw OHLCV data.
        """
        # TODO: Call yfinance with ticker, period, and interval.
        # TODO: Return provider data to fetch().
        pass
