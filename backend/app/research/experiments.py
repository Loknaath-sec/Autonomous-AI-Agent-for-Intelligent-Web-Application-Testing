from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ExperimentResult:
    experiment_id: str
    method: str
    website: str
    test_case: str
    model: str = "gpt-4o-mini"
    model_version: str = "N/A"
    prompt_version: str = "v1"
    browser: str = "chromium"
    configuration: dict[str, Any] = field(default_factory=dict)
    start_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    duration_seconds: float = 0.0
    total_steps: int = 0
    passed_steps: int = 0
    failed_steps: int = 0
    confirmed_bugs: int = 0
    false_positives: int = 0
    self_healed_actions: int = 0
    exploration_depth: int = 0
    pages_explored: int = 0
    llm_calls: int = 0
    notes: str = "NOT YET MEASURED"


class ExperimentFramework:
    def __init__(self):
        self.results: list[ExperimentResult] = []

    def run_experiment(self, method: str, website: str, test_case: str, **config: Any) -> ExperimentResult:
        result = ExperimentResult(
            experiment_id=f"exp-{len(self.results) + 1:04d}",
            method=method,
            website=website,
            test_case=test_case,
            configuration=config,
            prompt_version=config.get("prompt_version", "v1"),
        )
        self.results.append(result)
        return result

    def metrics_summary(self) -> dict[str, Any]:
        summary = {
            "task_success_rate": "NOT YET MEASURED",
            "bug_precision": "NOT YET MEASURED",
            "bug_recall": "NOT YET MEASURED",
            "false_positive_rate": "NOT YET MEASURED",
            "self_healing_rate": "NOT YET MEASURED",
            "test_coverage": "NOT YET MEASURED",
            "exploration_depth": "NOT YET MEASURED",
            "execution_time": "NOT YET MEASURED",
        }
        return summary
