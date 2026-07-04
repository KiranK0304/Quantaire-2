"""Factory functions for constructing application services."""

from app.analysis import AnalysisEngine
from app.charts import CandlestickChartGenerator
from app.config import AppConfig
from app.data import MarketDataFetcher, MarketDataNormalizer
from app.services.price_action import PriceActionAnalysisService
from app.vision import PatternDetector, VisionModelClient


def build_service(config: AppConfig) -> PriceActionAnalysisService:
    """
    Build the application's price action analysis service.

    Args:
        config: Application configuration.

    Returns:
        A fully configured PriceActionAnalysisService.
    """
    # Data layer.
    fetcher = MarketDataFetcher()
    normalizer = MarketDataNormalizer()

    # Chart layer.
    chart_generator = CandlestickChartGenerator()

    # Vision layer.
    vision_client = VisionModelClient(config.vision_model_name)
    detector = PatternDetector(vision_client)

    # Analysis layer.
    analysis_engine = AnalysisEngine()

    # Assemble the workflow service.
    return PriceActionAnalysisService(
        data_fetcher=fetcher,
        data_normalizer=normalizer,
        chart_generator=chart_generator,
        pattern_detector=detector,
        analysis_engine=analysis_engine,
    )
