"""Ticker validation skeletons for market data requests."""


class TickerValidator:
    """Validate ticker symbols before market data retrieval."""

    def __init__(self, allowed_suffixes: set[str] | None = None) -> None:
        """
        Create a ticker validator.

        Args:
            allowed_suffixes: Optional exchange suffixes allowed for ticker validation.
        """
        self.allowed_suffixes = allowed_suffixes

    def validate(self, ticker: str) -> str:
        """
        Validate and return a ticker symbol.

        Args:
            ticker: User-provided stock ticker.

        Returns:
            Validated ticker symbol.
        """
        # TODO: Receive request.normalized_ticker() output from MarketDataFetcher.fetch().
        # TODO: Reject empty ticker values before provider access.
        # TODO: Call self._has_allowed_suffix(ticker) when suffix rules are configured.
        # TODO: Return the validated ticker to MarketDataFetcher.fetch().
        pass

    def _has_allowed_suffix(self, ticker: str) -> bool:
        """
        Check whether a ticker suffix is allowed.

        Args:
            ticker: Normalized ticker symbol to inspect.

        Returns:
            True when no suffix restriction fails, otherwise False.
        """
        # TODO: Read self.allowed_suffixes configured in __init__().
        # TODO: Compare the ticker suffix against the configured suffix set.
        # TODO: Return the suffix decision to validate().
        pass
