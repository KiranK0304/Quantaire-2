from pathlib import Path

from app.config import AppConfig
from app.utils import ensure_directory
from app.services import build_service
from app.schemas import AnalysisReport, MarketDataRequest


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