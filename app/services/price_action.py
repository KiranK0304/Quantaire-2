"""Application service orchestration for the end-to-end analysis workflow."""

from pathlib import Path

from app.analysis import AnalysisEngine
from app.charts import CandlestickChartGenerator
from app.data import MarketDataFetcher, MarketDataNormalizer
from app.models import AnalysisReport, MarketDataRequest
from app.vision import PatternDetector


class PriceActionAnalysisService:
    """Coordinate data retrieval, chart generation, vision analysis, and reporting."""

    def __init__(
        self,
        data_fetcher: MarketDataFetcher | None = None,
        data_normalizer: MarketDataNormalizer | None = None,
        chart_generator: CandlestickChartGenerator | None = None,
        pattern_detector: PatternDetector | None = None,
        analysis_engine: AnalysisEngine | None = None,
    ) -> None:
        """
        Create the price action analysis service.

        Args:
            data_fetcher: Optional market data fetcher.
            data_normalizer: Optional market data normalizer.
            chart_generator: Optional candlestick chart generator.
            pattern_detector: Optional chart pattern detector.
            analysis_engine: Optional market analysis engine.
        """
        self.data_fetcher = data_fetcher or MarketDataFetcher()
        self.data_normalizer = data_normalizer or MarketDataNormalizer()
        self.chart_generator = chart_generator or CandlestickChartGenerator()
        self.pattern_detector = pattern_detector or PatternDetector()
        self.analysis_engine = analysis_engine or AnalysisEngine()

    def analyze_ticker(
        self,
        request: MarketDataRequest,
        chart_output_path: Path,
    ) -> AnalysisReport:
        """
        Run the full historical chart analysis workflow for a ticker.

        Args:
            request: Market data request including ticker and time range.
            chart_output_path: Location where the generated chart should be saved.

        Returns:
            Structured market analysis report.
        """
        raw_data = self.data_fetcher.fetch(request)
        normalized_data = self.data_normalizer.normalize(raw_data)
        chart_artifact = self.chart_generator.generate_chart(
            data=normalized_data,
            ticker=request.ticker,
            output_path=chart_output_path,
        )
        detections = self.pattern_detector.detect_patterns(chart_artifact.image_path)
        report = self.analysis_engine.generate_report(
            ticker=request.ticker,
            detections=detections,
        )
        return report
