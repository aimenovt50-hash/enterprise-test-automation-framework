from __future__ import annotations

import allure

from src.data.factories.base_factory import UserData
from src.pages.auth_page import AuthPage


class AuthFlow:
    """Orchestrates multi-step authentication scenarios."""

    def __init__(self, auth_page: AuthPage) -> None:
        self.auth_page = auth_page

    @allure.step("Register and verify account")
    def register_new_user(self, user: UserData) -> None:
        self.auth_page.register(user)
        self.auth_page.expect_registration_success()

    @allure.step("Login and verify session")
    def login_as(self, email: str, password: str) -> None:
        self.auth_page.login(email, password)
        self.auth_page.expect_login_success(email)

    @allure.step("Register, logout, and login again")
    def register_logout_and_login(self, user: UserData) -> None:
        self.register_new_user(user)
        self.auth_page.logout()
        self.login_as(user.email, user.password)
