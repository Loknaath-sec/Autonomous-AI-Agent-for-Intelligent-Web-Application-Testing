from __future__ import annotations

from pathlib import Path


class StorageService:
    """Simple storage abstraction for screenshots and report files."""

    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir or "./reports")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def ensure_dir(self, relative_path: str) -> Path:
        path = self.base_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def save_bytes(self, relative_path: str, data: bytes) -> str:
        path = self.ensure_dir(relative_path)
        path.write_bytes(data)
        return str(path)

    def save_text(self, relative_path: str, text: str) -> str:
        path = self.ensure_dir(relative_path)
        path.write_text(text, encoding="utf-8")
        return str(path)
