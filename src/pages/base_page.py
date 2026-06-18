from __future__ import annotations

import re

import allure
from playwright.sync_api import Locator, Page, expect

from src.config.settings import get_global_settings
from src.utils.retry import retry


class BasePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.timeout = get_global_settings().timeout_ms

    @allure.step("Open page: {path}")
    def open(self, path: str = "/") -> None:
        self.page.goto(f"{self.base_url}{path}")
        self.page.wait_for_load_state("domcontentloaded")

    @retry(max_attempts=3, delay_seconds=0.5, exceptions=(AssertionError,))
    def wait_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible(timeout=self.timeout)

    @allure.step("Click element")
    def click(self, locator: Locator) -> None:
        self.wait_visible(locator)
        locator.click()

    @allure.step("Fill input")
    def fill(self, locator: Locator, value: str) -> None:
        self.wait_visible(locator)
        locator.fill(value)

    @allure.step("Assert page title contains: {expected}")
    def expect_title_contains(self, expected: str) -> None:
        pattern = re.compile(re.escape(expected), re.IGNORECASE)
        expect(self.page).to_have_title(pattern, timeout=self.timeout)
