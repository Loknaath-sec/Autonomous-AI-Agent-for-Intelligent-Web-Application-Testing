from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import TestRun
from app.database.session import get_db

router = APIRouter(tags=["runs"])


class TestRunCreate(BaseModel):
    project_id: str | None = None
    instruction: str
    browser: str = "chromium"
    max_steps: int = 20
    max_depth: int = 4


@router.post("", status_code=status.HTTP_201_CREATED)
def create_run(payload: TestRunCreate, db: Session = Depends(get_db)) -> dict:
    run = TestRun(
        project_id=payload.project_id,
        instruction=payload.instruction,
        browser=payload.browser,
        max_steps=payload.max_steps,
        max_depth=payload.max_depth,
        status="pending",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return {"id": run.id, "status": run.status, "instruction": run.instruction}


@router.get("")
def list_runs(db: Session = Depends(get_db)) -> list[dict]:
    runs = db.query(TestRun).all()
    return [{"id": r.id, "status": r.status, "browser": r.browser, "instruction": r.instruction} for r in runs]


@router.get("/{run_id}")
def get_run(run_id: str, db: Session = Depends(get_db)) -> dict:
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    return {"id": run.id, "status": run.status, "instruction": run.instruction, "browser": run.browser}


@router.post("/{run_id}/cancel")
def cancel_run(run_id: str, db: Session = Depends(get_db)) -> dict:
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Test run not found")
    run.status = "cancelled"
    db.commit()
    return {"status": "cancelled", "id": run_id}
