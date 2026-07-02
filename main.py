"""Command-line entrypoint skeleton for the stock price action analyzer."""

import logging
from pathlib import Path

from app.config import AppConfig
from app.models import MarketDataRequest
from app.services import PriceActionAnalysisService
from app.utils.logging import configure_logging


def collect_market_data_input() -> MarketDataRequest:
    """
    Collect and validate market data request parameters.

    Returns:
        A validated market data request.

    Raises:
        ValidationError:
            If the provided input is invalid.
    """
    ticker = input("Ticker: ")
    period = input("Period [6mo]: ") or "6mo"
    interval = input("Interval [1d]: ") or "1d"

    return MarketDataRequest(
        ticker=ticker,
        period=period,
        interval=interval,
    )


def build_service(config: AppConfig) -> PriceActionAnalysisService:
    """
    Build the application service graph.

    Args:
        config: Runtime application configuration.

    Returns:
        Configured price action analysis service.
    """
    # TODO: Use config.vision_model_name to configure the vision model client.
    # TODO: Create concrete data, chart, vision, and analysis components.
    # TODO: Inject components into PriceActionAnalysisService.
    # TODO: Return the service to analyze_ticker().
    pass


def analyze_ticker(ticker: str, output_path: Path | None = None) -> None:
    """
    Analyze a ticker and emit a structured market analysis result.

    Args:
        ticker: Stock ticker to analyze.
        output_path: Optional chart image output path.

    Returns:
        None.
    """
    # TODO: Create AppConfig for default period, interval, and chart output directory.
    # TODO: Call build_service(config) to obtain the workflow service.
    # TODO: Create MarketDataRequest with ticker, config.default_period, and config.default_interval.
    # TODO: Resolve chart path from output_path or config.chart_path_for_ticker(ticker).
    # TODO: Call service.analyze_ticker(request, chart_path) to obtain AnalysisReport.
    # TODO: Hand the report to CLI output or future API response formatting.
    pass


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

    request = collect_market_data_input()

    # TODO: Pass parsed values into analyze_ticker().

    logger.info("Application finished.")

if __name__ == "__main__":
    main()
