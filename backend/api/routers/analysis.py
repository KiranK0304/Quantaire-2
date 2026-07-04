from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas import MarketDataRequest, AnalysisReport
from app.services import analyze_ticker
from app.config import AppConfig

router = APIRouter()


@router.post("/analyze", response_model=AnalysisReport)
def analyse(request: MarketDataRequest) -> AnalysisReport:
    report = analyze_ticker(request)
    return report


@router.get("/chart/{ticker}")
def get_chart(ticker: str) -> FileResponse:
    config = AppConfig()
    chart_path = config.chart_path_for_ticker(ticker.upper())
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail=f"Chart for {ticker} not found. Run analysis first.")
    return FileResponse(chart_path, media_type="image/png")


@router.get("/patterns")
def get_supported_patterns():
    return {
        "supported_patterns": [
            {"id": 0, "name": "Head and shoulders bottom", "type": "Bullish Reversal"},
            {"id": 1, "name": "Head and shoulders top", "type": "Bearish Reversal"},
            {"id": 2, "name": "M_Head", "type": "Double Top"},
            {"id": 3, "name": "StockLine", "type": "Trendline / Support & Resistance"},
            {"id": 4, "name": "Triangle", "type": "Consolidation"},
            {"id": 5, "name": "W_Bottom", "type": "Double Bottom"}
        ]
    }
