from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys

# Ensure the parent directory is in sys.path so we can import the existing pipeline
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.analyze import analyze_single

app = FastAPI(title="Pattern Detection Web App")

# Mount frontend static files (CSS, Images)
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "web" / "static")), name="static")


# Mount the backend outputs directory so annotated images can be served directly to the browser
app.mount("/outputs", StaticFiles(directory=str(PROJECT_ROOT / "outputs")), name="outputs")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "web" / "templates"))
EXPECTED_RANGES = ("1M", "3M", "6M", "1Y")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage search box."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, ticker: str = Form(...)):
    """Handle form submission, run pipeline, and render results."""
    ticker = ticker.strip().upper()
    
    # Run the existing backend pipeline asynchronously
    # (Since this is a lightweight wrapper, we reuse the exact function)
    try:
        results = await analyze_single(ticker, multi_range=True)
        
        if not results:
            return templates.TemplateResponse(request=request, name="results.html", context={
                "ticker": ticker,
                "error": "Failed to analyze ticker. Make sure the symbol is valid."
            })
            
        # Clean up absolute paths so they can be served by the mounted /outputs route
        for r in results:
            if "output_path" in r and r["output_path"]:
                abs_path = Path(r["output_path"])
                try:
                    # Convert absolute path (e.g. /home/user/proj/outputs/...) 
                    # into a relative URL (outputs/...)
                    rel_path = abs_path.relative_to(PROJECT_ROOT)
                    r["output_path"] = str(rel_path).replace("\\", "/")
                except ValueError:
                    pass

        result_by_range = {r.get("timeframe"): r for r in results}
        results = [
            result_by_range.get(timeframe, {
                "timeframe": timeframe,
                "detected": False,
                "output_path": None,
                "message": "Chart capture did not return an image for this range."
            })
            for timeframe in EXPECTED_RANGES
        ]

        return templates.TemplateResponse(request=request, name="results.html", context={
            "ticker": ticker,
            "results": results
        })
        
    except Exception as e:
        return templates.TemplateResponse(request=request, name="results.html", context={
            "ticker": ticker,
            "error": f"An internal error occurred: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    # Run development server
    uvicorn.run("app:app", host="127.0.0.1", port=8800, reload=True)
