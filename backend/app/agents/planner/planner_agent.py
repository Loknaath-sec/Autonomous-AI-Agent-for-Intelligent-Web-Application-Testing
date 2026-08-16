from __future__ import annotations

import json
from typing import Any

from app.llm.openai_provider import OpenAICompatibleProvider
from app.llm.schemas import PlannerPlan


class PlannerAgent:
    def __init__(self, llm_provider: OpenAICompatibleProvider | None = None):
        self.llm_provider = llm_provider or OpenAICompatibleProvider()

    def create_plan(self, instruction: str, website_url: str) -> PlannerPlan:
        prompt = f"""
        You are the Planner Agent for the Autonomous AI Agent for Intelligent Web Application Testing platform.
        Convert the user's natural-language instruction into a structured test plan.

        Website URL: {website_url}
        Instruction: {instruction}

        Return valid JSON matching the schema.
        The plan should contain a goal and a list of tasks with ids, descriptions, types, expected results, dependencies, and a risk level.
        Focus on realistic web testing workflows and avoid destructive or unauthorized actions.
        """
        response = self.llm_provider.generate(prompt, response_model=PlannerPlan)
        if isinstance(response, str):
            data = json.loads(response)
            response = PlannerPlan.model_validate(data)
        return response
