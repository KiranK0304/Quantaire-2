"""Command-line entrypoint skeleton for the stock price action analyzer."""

import logging
from pathlib import Path

from app.config import AppConfig
from app.models import AnalysisReport, MarketDataRequest
from app.services import build_service
from app.utils import configure_logging, ensure_directory


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


def analyze_ticker(
    request: MarketDataRequest,
    output_path: Path | None = None,
    config: AppConfig | None = None,
) -> AnalysisReport:
    """
    Analyze a stock ticker using the configured application workflow.

    Args:
        request: Validated market data request.
        output_path: Optional location where the generated chart should be saved.

    Returns:
        A structured analysis report.
    """
    config = config or AppConfig()

    service = build_service(config)

    chart_path = (
        Path(output_path)
        if output_path is not None
        else config.chart_path_for_ticker(request.ticker)
    )
    ensure_directory(chart_path.parent)

    report = service.analyze_ticker(request, chart_path)

    return report


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
