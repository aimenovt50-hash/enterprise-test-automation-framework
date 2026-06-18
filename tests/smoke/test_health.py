import allure
import pytest


@pytest.mark.smoke
@allure.story("Health")
@allure.title("Home page loads successfully")
def test_home_page_loads(dashboard_page):
    dashboard_page.open_home()
    dashboard_page.expect_loaded()


@pytest.mark.smoke
@allure.story("Search")
@allure.title("Product search returns results page")
def test_product_search(dashboard_page):
    dashboard_page.open_home()
    dashboard_page.search("computer")
    dashboard_page.expect_title_contains("Search")
