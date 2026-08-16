from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InteractiveElement:
    selector: str | None = None
    role: str | None = None
    name: str | None = None
    text: str | None = None
    href: str | None = None
    type: str | None = None


@dataclass
class WebPageState:
    url: str
    title: str
    visible_text: str
    dom_summary: str
    interactive_elements: list[InteractiveElement] = field(default_factory=list)
    forms: list[str] = field(default_factory=list)
    buttons: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    accessibility_information: dict[str, Any] = field(default_factory=dict)
    screenshot_path: str | None = None
    browser_state: dict[str, Any] = field(default_factory=dict)


class PerceptionAgent:
    def normalize_page_state(self, **data: Any) -> WebPageState:
        return WebPageState(
            url=data.get("url", ""),
            title=data.get("title", ""),
            visible_text=data.get("visible_text", ""),
            dom_summary=data.get("dom_summary", ""),
            interactive_elements=[InteractiveElement(**item) for item in data.get("interactive_elements", [])],
            forms=data.get("forms", []),
            buttons=data.get("buttons", []),
            links=data.get("links", []),
            inputs=data.get("inputs", []),
            accessibility_information=data.get("accessibility_information", {}),
            screenshot_path=data.get("screenshot_path"),
            browser_state=data.get("browser_state", {}),
        )
