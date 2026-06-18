from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardLocators:
    header_logo: str = ".header-logo"
    search_box: str = "#small-searchterms"
    search_button: str = "input[type='submit'][value='Search']"
    account_link: str = "a.account"
