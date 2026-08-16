from pydantic import BaseModel, Field


class PlannerTask(BaseModel):
    id: int
    description: str
    type: str
    expected_result: str
    dependencies: list[int] = Field(default_factory=list)
    risk_level: str = "medium"


class PlannerPlan(BaseModel):
    goal: str
    tasks: list[PlannerTask]


class BrowserAction(BaseModel):
    action: str
    target: dict | None = None
    reason: str
    confidence: float = 0.0
    metadata: dict | None = None


class VerificationResult(BaseModel):
    status: str
    classification: str
    details: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class BugReport(BaseModel):
    title: str
    bug_type: str
    severity: str
    confidence: float = 0.0
    description: str
    expected_result: str
    actual_result: str
    reproduction_steps: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    root_cause_hypothesis: str
    suggested_fix: str
