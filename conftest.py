"""
conftest.py
-----------
Root-level Pytest configuration and shared fixtures for the WebTestX
framework.  Fixtures defined here are available to every test module
without any explicit import.
"""

import json
import os
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from utils.api_client import APIClient
from utils.config import config
from utils.logger import get_logger

logger = get_logger("conftest")


# ======================================================================
#  Session-level: ensure output directories exist
# ======================================================================

def pytest_configure(config: pytest.Config) -> None:
    """Create reports and screenshots directories before any test runs."""
    from utils.config import config as app_config
    Path(app_config.REPORTS_DIR).mkdir(parents=True, exist_ok=True)
    Path(app_config.SCREENSHOTS_DIR).mkdir(parents=True, exist_ok=True)


# ======================================================================
#  API Fixtures
# ======================================================================

@pytest.fixture(scope="session")
def api_client() -> Generator[APIClient, None, None]:
    """
    Session-scoped APIClient instance.

    The same HTTP session is reused for all API tests in the run,
    which is both faster and more realistic.
    """
    logger.info("Creating APIClient (base_url=%s)", config.API_BASE_URL)
    client = APIClient(base_url=config.API_BASE_URL)
    yield client
    client.close()
    logger.info("APIClient session closed.")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the API base URL from configuration."""
    return config.API_BASE_URL


# ======================================================================
#  Test Data Fixture
# ======================================================================

@pytest.fixture(scope="session")
def test_data() -> dict:
    """
    Load and return the test-data JSON file as a Python dict.

    The fixture is session-scoped so the file is read only once per run.
    """
    data_path = Path(config.TEST_DATA_PATH)
    logger.info("Loading test data from: %s", data_path)
    with data_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


# ======================================================================
#  Playwright / UI Fixtures
# ======================================================================

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Start and stop the Playwright engine once per test session."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Launch the configured browser once per session.

    Uses the BROWSER and HEADLESS settings from ``Config``.
    """
    browser_type = getattr(playwright_instance, config.BROWSER)
    launched = browser_type.launch(headless=config.HEADLESS)
    logger.info(
        "Browser launched: %s  (headless=%s)", config.BROWSER, config.HEADLESS
    )
    yield launched
    launched.close()
    logger.info("Browser closed.")


@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Create a fresh browser context (isolated state) for each test function.

    This ensures cookies, localStorage, and session state are reset
    between individual UI tests.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        accept_downloads=True,
    )
    context.set_default_timeout(config.PAGE_TIMEOUT_MS)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    """Return a new Playwright Page for each test function."""
    pg = browser_context.new_page()
    yield pg
    pg.close()


# ======================================================================
#  Failure Evidence: Screenshots on UI test failure
# ======================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    After each test call phase, capture a screenshot if a UI test has failed.
    The screenshot is saved to the screenshots directory for debugging.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Only attempt screenshot if a Playwright page fixture is active
        page_fixture = item.funcargs.get("page")
        if page_fixture is not None:
            screenshot_path = os.path.join(
                config.SCREENSHOTS_DIR,
                f"FAIL_{item.name}.png",
            )
            try:
                page_fixture.screenshot(path=screenshot_path, full_page=True)
                logger.warning(
                    "Screenshot captured for failed test: %s → %s",
                    item.name,
                    screenshot_path,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("Could not capture screenshot: %s", exc)
