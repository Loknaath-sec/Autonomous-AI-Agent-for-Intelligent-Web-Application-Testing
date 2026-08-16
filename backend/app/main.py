from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings
from app.database.init_db import init_db

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous AI web testing platform for research and validation.",
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


@app.get("/api/health")
def api_health() -> dict:
    return {
        "status": "healthy",
        "version": settings.app_version,
    }
