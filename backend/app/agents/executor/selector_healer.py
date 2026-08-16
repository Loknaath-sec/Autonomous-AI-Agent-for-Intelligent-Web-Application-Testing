from __future__ import annotations

from typing import Any


class SelectorHealer:
    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold

    def heal(self, original_selector: str, candidates: list[dict[str, Any]]) -> dict[str, Any]:
        for candidate in candidates:
            score = float(candidate.get("confidence", 0.0))
            if score >= self.confidence_threshold:
                return {
                    "original_selector": original_selector,
                    "replacement_selector": candidate.get("selector") or candidate.get("name") or original_selector,
                    "confidence": score,
                    "evidence": candidate.get("evidence", []),
                    "healed": True,
                }
        return {
            "original_selector": original_selector,
            "replacement_selector": original_selector,
            "confidence": 0.0,
            "evidence": [],
            "healed": False,
        }
