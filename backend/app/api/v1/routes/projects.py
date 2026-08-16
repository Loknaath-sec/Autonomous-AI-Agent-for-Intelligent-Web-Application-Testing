from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.models import Project
from app.database.session import get_db

router = APIRouter(tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    url: str


@router.get("")
def list_projects(db: Session = Depends(get_db)) -> list[dict]:
    projects = db.query(Project).all()
    return [{"id": p.id, "name": p.name, "url": p.url} for p in projects]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> dict:
    project = Project(name=payload.name, url=payload.url, owner_id="system")
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "url": project.url}


@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "name": project.name, "url": project.url}


@router.delete("/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted", "id": project_id}
