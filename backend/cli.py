"""Command-line entrypoint skeleton for the stock price action analyzer."""

import logging

from app.config import AppConfig
from app.services import analyze_ticker
from app.utils import configure_logging
from app.schemas import MarketDataRequest



def collect_market_data_input(config: AppConfig) -> MarketDataRequest:
    """
    Collect and validate market data request parameters.

    Args:
        config: Application configuration providing default request values.

    Returns:
        A validated market data request.

    Raises:
        ValidationError:
            If the provided input is invalid.
    """
    ticker = input("Ticker: ")
    period = input(f"Period [{config.default_period}]: ") or config.default_period
    interval = input(
        f"Interval [{config.default_interval}]: "
    ) or config.default_interval

    return MarketDataRequest(
        ticker=ticker,
        period=period,
        interval=interval,
    )



def main() -> None:
    """
    Run the application entry point.

    Returns:
        None.
    """
    # Configure application-wide logging.
    configure_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting Price Action Analyzer.")

    config = AppConfig()
    request = collect_market_data_input(config)

    report = analyze_ticker(request, config=config)
    logger.info("Analysis complete for %s", report.ticker)
    logger.info("Summary: %s", report.summary)
    logger.debug("Report metadata: %s", report.metadata)

    logger.info("Application finished.")

if __name__ == "__main__":
    main()
