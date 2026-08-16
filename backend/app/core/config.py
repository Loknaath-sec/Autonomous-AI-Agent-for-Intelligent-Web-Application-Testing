from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Autonomous AI Agent for Intelligent Web Application Testing"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"
    environment: str = "development"
    database_url: str = "sqlite:///./websentinel.db"
    jwt_secret: str = "change-me-in-production"
    secret_key: str = "change-me-in-production"
    openai_api_key: str = ""
    playwright_headless: bool = True
    max_steps: int = 20
    max_depth: int = 4
    max_pages: int = 10
    max_execution_time: int = 300
    allowed_origins: List[str] = Field(default_factory=lambda: [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:3000",
    ])
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
