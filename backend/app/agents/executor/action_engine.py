from __future__ import annotations

from typing import Any


class ActionEngine:
    def __init__(self, confidence_threshold: float = 0.85):
        self.confidence_threshold = confidence_threshold

    def validate_action(self, action: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(action, dict):
            raise ValueError("Action must be a dictionary")
        if "action" not in action:
            raise ValueError("Action is missing required 'action' field")
        if action.get("confidence", 0) < self.confidence_threshold:
            raise ValueError("Action confidence fell below the configured threshold.")
        return action
