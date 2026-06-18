from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthLocators:
    register_link: str = "a[href='/register']"
    login_link: str = "a[href='/login']"
    first_name: str = "#FirstName"
    last_name: str = "#LastName"
    email: str = "#Email"
    password: str = "#Password"
    confirm_password: str = "#ConfirmPassword"
    register_button: str = "#register-button"
    login_button: str = "input.button-1.login-button"
    account_link: str = "a.account"
    registration_result: str = ".result"
    logout_link: str = "a[href='/logout']"
