from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.models import Bug
from app.database.session import get_db

router = APIRouter(tags=["bugs"])


@router.get("")
def list_bugs(db: Session = Depends(get_db)) -> list[dict]:
    bugs = db.query(Bug).all()
    return [{"id": b.id, "title": b.title, "severity": b.severity, "bug_type": b.bug_type, "status": b.status} for b in bugs]


@router.get("/{bug_id}")
def get_bug(bug_id: str, db: Session = Depends(get_db)) -> dict:
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return {"id": bug.id, "title": bug.title, "severity": bug.severity, "bug_type": bug.bug_type, "description": bug.description, "status": bug.status}
