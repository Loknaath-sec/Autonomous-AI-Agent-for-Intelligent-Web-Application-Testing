from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, response_model: type[BaseModel] | None = None, **kwargs: Any) -> Any:
        """Generate structured output for a prompt."""

    @abstractmethod
    def validate(self, payload: Any, response_model: type[BaseModel]) -> BaseModel:
        """Validate and normalize model response payloads."""
