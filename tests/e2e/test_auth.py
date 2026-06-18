import allure
import pytest

from src.data.factories.base_factory import UserFactory
from src.flows.auth_flow import AuthFlow


@pytest.mark.e2e
@pytest.mark.auth
@allure.story("Registration")
@allure.title("Registration form is accessible")
def test_user_registration_form(auth_page):
    auth_page.open_register()
    auth_page.expect_registration_form_visible()


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.regression
@allure.story("Registration")
@allure.title("User registers with generated test data")
def test_user_registration_with_factory(auth_flow: AuthFlow):
    user = UserFactory.build()
    auth_flow.register_new_user(user)


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.regression
@allure.story("Login")
@allure.title("Registered user can log in")
def test_user_login_after_registration(auth_flow: AuthFlow, user_data):
    auth_flow.register_logout_and_login(user_data)


@pytest.mark.e2e
@pytest.mark.auth
@pytest.mark.negative
@allure.story("Login")
@allure.title("Invalid credentials show validation error")
def test_login_with_invalid_password(auth_page, registered_user):
    auth_page.login(registered_user.email, "WrongPass123!")
    auth_page.expect_title_contains("Login")
