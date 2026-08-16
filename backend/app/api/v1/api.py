from fastapi import APIRouter

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.bugs import router as bugs_router
from app.api.v1.routes.experiments import router as experiments_router
from app.api.v1.routes.projects import router as projects_router
from app.api.v1.routes.reports import router as reports_router
from app.api.v1.routes.runs import router as runs_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(projects_router, prefix="/projects")
api_router.include_router(runs_router, prefix="/test-runs")
api_router.include_router(bugs_router, prefix="/bugs")
api_router.include_router(reports_router, prefix="/reports")
api_router.include_router(experiments_router, prefix="/experiments")
