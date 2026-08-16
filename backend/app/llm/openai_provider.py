import json
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import get_settings
from app.llm.base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key or get_settings().openai_api_key
        self.base_url = base_url or "https://api.openai.com/v1"
        self.client = httpx.Client(timeout=30.0)

    def generate(self, prompt: str, response_model: type[BaseModel] | None = None, **kwargs: Any) -> Any:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        payload = {
            "model": kwargs.get("model", "gpt-4o-mini"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.2),
        }
        if response_model is not None:
            payload["response_format"] = {"type": "json_schema", "json_schema": {"name": "response", "schema": response_model.model_json_schema()}}

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        response = self.client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return content

        if response_model is not None:
            return self.validate(parsed, response_model)
        return parsed

    def validate(self, payload: Any, response_model: type[BaseModel]) -> BaseModel:
        try:
            return response_model.model_validate(payload)
        except ValidationError:
            fallback = self._safe_parse(payload)
            if fallback is None:
                raise ValueError("LLM output could not be safely parsed.")
            try:
                return response_model.model_validate(fallback)
            except ValidationError as exc:
                raise ValueError("LLM output failed validation after safe parsing.") from exc

    def _safe_parse(self, payload: Any) -> Any:
        if isinstance(payload, dict):
            return payload
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return None
        return None
