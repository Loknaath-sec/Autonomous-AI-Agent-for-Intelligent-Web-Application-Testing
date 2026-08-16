from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from playwright.async_api import async_playwright


class BrowserExecutor:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(viewport={"width": 1440, "height": 1200})
        self.page = await self.context.new_page()

    async def stop(self):
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()

    async def goto(self, url: str):
        await self.page.goto(url, wait_until="domcontentloaded")

    async def click(self, selector: str):
        await self.page.click(selector)

    async def fill(self, selector: str, value: str):
        await self.page.fill(selector, value)

    async def press(self, selector: str, key: str):
        await self.page.press(selector, key)

    async def hover(self, selector: str):
        await self.page.hover(selector)

    async def scroll(self, y: int = 0):
        await self.page.evaluate(f"window.scrollTo(0, {y})")

    async def wait_for_element(self, selector: str, timeout: int = 15000):
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def take_screenshot(self, path: str):
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        await self.page.screenshot(path=str(target), full_page=True)
        return str(target)

    async def get_dom(self) -> str:
        return await self.page.content()

    async def get_console_logs(self):
        return self.page.on("console", lambda msg: msg)

    async def get_network_logs(self):
        return []

    async def get_page_info(self) -> dict[str, Any]:
        return {
            "url": self.page.url,
            "title": await self.page.title(),
            "visible_text": await self.page.locator("body").inner_text(),
        }
