from __future__ import annotations

import allure
from playwright.sync_api import Page, expect

from src.pages.base_page import BasePage
from src.pages.locators.dashboard_locators import DashboardLocators


class DashboardPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.locators = DashboardLocators()

    @allure.step("Open home dashboard")
    def open_home(self) -> None:
        self.open("/")

    @allure.step("Search for product: {query}")
    def search(self, query: str) -> None:
        self.fill(self.page.locator(self.locators.search_box), query)
        self.click(self.page.locator(self.locators.search_button))

    @allure.step("Assert dashboard is loaded")
    def expect_loaded(self) -> None:
        self.wait_visible(self.page.locator(self.locators.header_logo))
        expect(self.page).to_have_url(f"{self.base_url}/")
