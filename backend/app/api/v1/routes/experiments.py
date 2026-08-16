from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import Experiment
from app.database.session import get_db

router = APIRouter(tags=["experiments"])


class ExperimentCreate(BaseModel):
    name: str
    method: str
    website: str
    test_case: str


@router.get("")
def list_experiments(db: Session = Depends(get_db)) -> list[dict]:
    experiments = db.query(Experiment).all()
    return [{"id": e.id, "name": e.name, "method": e.method, "website": e.website} for e in experiments]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_experiment(payload: ExperimentCreate, db: Session = Depends(get_db)) -> dict:
    experiment = Experiment(
        name=payload.name,
        method=payload.method,
        website=payload.website,
        test_case=payload.test_case,
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return {"id": experiment.id, "name": experiment.name, "method": experiment.method}
