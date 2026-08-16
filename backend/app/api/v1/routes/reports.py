from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.agents.reporter.report_generator import ReportGenerator
from app.database.models import Report
from app.database.session import get_db

router = APIRouter(tags=["reports"])


class ReportRequest(BaseModel):
    url: str
    instruction: str
    title: str | None = None


@router.post("/generate")
def generate_report(payload: ReportRequest, db: Session = Depends(get_db)) -> dict:
    title = payload.title or f"Autonomous AI Agent for Intelligent Web Application Testing Report - {payload.url}"
    generator = ReportGenerator()
    findings = generator.summarize_findings(payload.url, payload.instruction)
    report_path = generator.generate_html_report(title=title, content=findings)

    report = Report(
        title=title,
        format="html",
        file_path=report_path,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    with open(report_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    return {
        "status": "success",
        "report_id": report.id,
        "report_path": report_path,
        "report_html": html_content,
    }


@router.get("/download/{report_id}")
def download_report(report_id: str, db: Session = Depends(get_db)) -> FileResponse:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    file_path = Path(report.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(file_path, media_type="application/pdf", filename=file_path.name)


@router.get("/{report_id}")
def get_report(report_id: str, db: Session = Depends(get_db)) -> dict:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"id": report.id, "title": report.title, "format": report.format, "file_path": report.file_path}
