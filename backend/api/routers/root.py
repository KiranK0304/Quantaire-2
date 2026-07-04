from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
  "name": "Price Action Analyzer API",
  "version": "1.0.0",
  "description": "AI-powered stock price action analysis service.",
  "docs": "/docs"
}