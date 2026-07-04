from fastapi import FastAPI

from .routers import analysis, root, health

app = FastAPI()

app.include_router(root.router)
app.include_router(health.router)
app.include_router(analysis.router)