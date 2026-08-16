from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.database.models import MemoryEntry


class MemoryService:
    def __init__(self, db: Session):
        self.db = db

    def store_short_term(self, run_id: str | None, key: str, value: Any) -> MemoryEntry:
        entry = MemoryEntry(run_id=run_id, key=key, value=str(value), memory_type="short_term")
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def store_long_term(self, run_id: str | None, key: str, value: Any) -> MemoryEntry:
        entry = MemoryEntry(run_id=run_id, key=key, value=str(value), memory_type="long_term")
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_recent(self, run_id: str | None = None, limit: int = 20) -> list[MemoryEntry]:
        query = self.db.query(MemoryEntry)
        if run_id:
            query = query.filter(MemoryEntry.run_id == run_id)
        return query.order_by(MemoryEntry.created_at.desc()).limit(limit).all()

    def relevant_memory(self, current_task: str, website: str | None = None, limit: int = 10) -> list[MemoryEntry]:
        query = self.db.query(MemoryEntry).filter(
            MemoryEntry.key.contains("task")
            | MemoryEntry.value.contains(current_task[:80])
        )
        if website:
            query = query.filter(MemoryEntry.value.contains(website))
        return query.order_by(MemoryEntry.created_at.desc()).limit(limit).all()
