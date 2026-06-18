import allure
import pytest

from tests.conftest import require_feature


@pytest.mark.regression
@pytest.mark.dashboard
@allure.story("Search")
@allure.title("Search for books category")
def test_search_books(dashboard_page, env_config):
    require_feature(env_config, "new_dashboard")
    dashboard_page.open_home()
    dashboard_page.search("book")
    dashboard_page.expect_title_contains("Search")


@pytest.mark.regression
@pytest.mark.dashboard
@allure.story("Branding")
@allure.title("Logo is visible on dashboard")
def test_dashboard_branding(dashboard_page):
    dashboard_page.open_home()
    dashboard_page.expect_loaded()
