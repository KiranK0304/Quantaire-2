from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import (
    MarketDataNotFoundError,
    DataNormalizationError,
    ChartGenerationError,
    VisionInferenceError,
    PriceActionAnalyzerError,
)
from .routers import analysis, root, health

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(MarketDataNotFoundError)
async def market_data_not_found_exception_handler(request: Request, exc: MarketDataNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "detail": str(exc)},
    )


@app.exception_handler(DataNormalizationError)
async def data_normalization_exception_handler(request: Request, exc: DataNormalizationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Unprocessable Entity", "detail": str(exc)},
    )


@app.exception_handler(PriceActionAnalyzerError)
async def price_action_analyzer_exception_handler(request: Request, exc: PriceActionAnalyzerError):
    # Catch-all for other domain exceptions like ChartGenerationError and VisionInferenceError
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)},
    )


app.include_router(root.router)
app.include_router(health.router)
app.include_router(analysis.router)