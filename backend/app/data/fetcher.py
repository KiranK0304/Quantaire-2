"""Historical market data retrieval."""

import yfinance as yf
from typing import TYPE_CHECKING

from app.schemas import MarketDataRequest, StockInfo
from app.exceptions import MarketDataNotFoundError

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
            raise MarketDataNotFoundError(ticker)

        return data

    def fetch_info(self, ticker: str) -> "StockInfo":
        """
        Fetch company and stock information from the configured provider.

        Args:
            ticker: Validated ticker symbol.

        Returns:
            StockInfo schema populated with Yahoo Finance data.
        """
        from app.schemas.schemas import StockInfo
        
        info = yf.Ticker(ticker).info
        # Basic check to see if the ticker exists at all in YF
        if not info or ("shortName" not in info and "longName" not in info):
            raise MarketDataNotFoundError(ticker)
            
        return StockInfo(
            # General Info
            long_name=info.get("longName") or info.get("shortName"),
            sector=info.get("sector"),
            industry=info.get("industry"),
            summary=info.get("longBusinessSummary"),
            website=info.get("website"),
            currency=info.get("currency"),
            
            # Daily Price Action
            previous_close=info.get("previousClose"),
            open_price=info.get("open"),
            day_low=info.get("dayLow"),
            day_high=info.get("dayHigh"),
            volume=info.get("volume"),
            average_volume=info.get("averageVolume"),
            
            # Technical & Moving Averages
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
            fifty_day_average=info.get("fiftyDayAverage"),
            two_hundred_day_average=info.get("twoHundredDayAverage"),
            
            # Valuation & Dividends
            market_cap=info.get("marketCap"),
            enterprise_value=info.get("enterpriseValue"),
            trailing_pe=info.get("trailingPE"),
            forward_pe=info.get("forwardPE"),
            price_to_book=info.get("priceToBook"),
            dividend_yield=info.get("dividendYield"),
            
            # Financial Health & Growth
            profit_margins=info.get("profitMargins"),
            operating_margins=info.get("operatingMargins"),
            return_on_equity=info.get("returnOnEquity"),
            revenue_growth=info.get("revenueGrowth"),
            earnings_growth=info.get("earningsGrowth"),
            debt_to_equity=info.get("debtToEquity")
        )