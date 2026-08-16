from __future__ import annotations

from typing import Any


class BugAnalyzer:
    def analyze(self, verification_result: dict[str, Any], expected_result: str, observed_result: str) -> dict[str, Any]:
        if verification_result.get("classification") == "WEBSITE_DEFECT":
            return {
                "title": "Website behavior does not match expected result",
                "bug_type": "Functional",
                "severity": "High",
                "confidence": verification_result.get("confidence", 0.0),
                "description": "The system observed a mismatch between the expected and actual web behavior.",
                "expected_result": expected_result,
                "actual_result": observed_result,
                "reproduction_steps": ["Observe expected action", "Execute user flow", "Compare actual UI state"],
                "evidence": verification_result.get("evidence", []),
                "root_cause_hypothesis": "The page or app logic produced an unexpected state or route.",
                "suggested_fix": "Inspect the relevant page logic and confirm the expected behavior is implemented consistently.",
                "verification_status": "CONFIRMED_EVIDENCE",
            }
        return {
            "title": "No confirmed website bug detected",
            "bug_type": "None",
            "severity": "Informational",
            "confidence": 0.0,
            "description": "The failure was not confirmed as a website defect after verification.",
            "expected_result": expected_result,
            "actual_result": observed_result,
            "reproduction_steps": [],
            "evidence": verification_result.get("evidence", []),
            "root_cause_hypothesis": "No confirmed defect found; behavior may be due to automation or environmental factors.",
            "suggested_fix": "Review browser logs, retry, or inspect the page state.",
            "verification_status": "AI_HYPOTHESIS",
        }
