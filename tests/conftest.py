from __future__ import annotations

from pathlib import Path

import allure
import pytest
from faker import Faker
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.config.settings import (
    EnvironmentConfig,
    get_environment_config,
    get_global_settings,
    get_runtime_settings,
)
from src.data.factories.base_factory import UserData, UserFactory
from src.flows.auth_flow import AuthFlow
from src.pages.auth_page import AuthPage
from src.pages.dashboard_page import DashboardPage

ARTIFACTS_DIR = Path("artifacts")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Target environment")


def pytest_configure(config):
    Faker.seed(config.getoption("--env") or get_runtime_settings().env)


@pytest.fixture(scope="session")
def env_name(pytestconfig) -> str:
    return pytestconfig.getoption("--env") or get_runtime_settings().env


@pytest.fixture(scope="session")
def env_config(env_name: str) -> EnvironmentConfig:
    return get_environment_config(env_name)


@pytest.fixture(scope="session")
def base_url(env_config: EnvironmentConfig) -> str:
    return env_config.base_url


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    runtime = get_runtime_settings()
    browser_type = getattr(playwright_instance, runtime.browser)
    browser = browser_type.launch(headless=runtime.headless, slow_mo=runtime.slow_mo)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, env_config: EnvironmentConfig) -> BrowserContext:
    reporting = get_global_settings().reporting
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        record_video_dir=str(ARTIFACTS_DIR / "videos") if reporting.video_on_failure else None,
    )
    if reporting.trace_on_failure:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    page.set_default_timeout(get_runtime_settings().default_timeout)
    return page


@pytest.fixture(autouse=True)
def attach_environment(env_config: EnvironmentConfig):
    allure.dynamic.epic("Enterprise SaaS")
    allure.dynamic.feature(env_config.name)
    allure.dynamic.parameter("environment", env_config.name)


@pytest.fixture(autouse=True)
def capture_artifacts_on_failure(request, page: Page, context: BrowserContext):
    settings = get_global_settings().reporting
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if not rep_call or not rep_call.failed:
        return

    if settings.screenshots_on_failure:
        screenshot_dir = ARTIFACTS_DIR / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    if settings.trace_on_failure:
        trace_dir = ARTIFACTS_DIR / "traces"
        trace_dir.mkdir(parents=True, exist_ok=True)
        trace_path = trace_dir / f"{request.node.name}.zip"
        context.tracing.stop(path=str(trace_path))
        allure.attach.file(str(trace_path), name="playwright_trace")


def require_feature(env_config: EnvironmentConfig, feature: str) -> None:
    if not env_config.features.get(feature, False):
        pytest.skip(f"Feature '{feature}' disabled for {env_config.name}")


@pytest.fixture()
def user_data() -> UserData:
    return UserFactory.build()


@pytest.fixture()
def auth_page(page: Page, base_url: str) -> AuthPage:
    return AuthPage(page, base_url)


@pytest.fixture()
def dashboard_page(page: Page, base_url: str) -> DashboardPage:
    return DashboardPage(page, base_url)


@pytest.fixture()
def auth_flow(auth_page: AuthPage) -> AuthFlow:
    return AuthFlow(auth_page)


@pytest.fixture()
def registered_user(auth_flow: AuthFlow, user_data: UserData) -> UserData:
    auth_flow.register_new_user(user_data)
    return user_data
