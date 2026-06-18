from __future__ import annotations

import re

import allure
from playwright.sync_api import Page, expect

from src.data.factories.base_factory import UserData
from src.pages.base_page import BasePage
from src.pages.locators.auth_locators import AuthLocators


class AuthPage(BasePage):
    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)
        self.locators = AuthLocators()

    @allure.step("Open registration page")
    def open_register(self) -> None:
        self.open("/register")

    @allure.step("Open login page")
    def open_login(self) -> None:
        self.open("/login")

    @allure.step("Register new user")
    def register(self, user: UserData) -> None:
        self.open_register()
        self.fill(self.page.locator(self.locators.first_name), user.first_name)
        self.fill(self.page.locator(self.locators.last_name), user.last_name)
        self.fill(self.page.locator(self.locators.email), user.email)
        self.fill(self.page.locator(self.locators.password), user.password)
        self.fill(self.page.locator(self.locators.confirm_password), user.password)
        self.click(self.page.locator(self.locators.register_button))

    @allure.step("Login with credentials")
    def login(self, email: str, password: str) -> None:
        self.open_login()
        self.fill(self.page.locator(self.locators.email), email)
        self.fill(self.page.locator(self.locators.password), password)
        self.click(self.page.locator(self.locators.login_button))

    @allure.step("Logout current user")
    def logout(self) -> None:
        self.click(self.page.locator(self.locators.logout_link))

    @allure.step("Assert registration succeeded")
    def expect_registration_success(self) -> None:
        expect(self.page).to_have_url(
            re.compile(r".*/registerresult/\d+", re.IGNORECASE),
            timeout=self.timeout,
        )
        expect(self.page.locator(self.locators.registration_result)).to_contain_text(
            "registration completed",
            ignore_case=True,
        )

    @allure.step("Assert login succeeded for {email}")
    def expect_login_success(self, email: str) -> None:
        account = self.page.get_by_role("link", name=email)
        self.wait_visible(account)
        expect(account).to_be_visible()

    @allure.step("Assert registration form is displayed")
    def expect_registration_form_visible(self) -> None:
        self.wait_visible(self.page.locator(self.locators.register_button))
