"""
utils/config.py
---------------
Central configuration for the WebTestX framework.
All environment-specific settings are managed here so that tests
never embed magic strings directly.
"""

import os


class Config:
    """
    Framework-wide configuration.

    Values are first read from environment variables so that CI/CD
    pipelines can override them without code changes.
    """

    # ------------------------------------------------------------------ #
    #  Base URLs
    # ------------------------------------------------------------------ #

    # JSONPlaceholder — public REST API used for API & regression tests
    API_BASE_URL: str = os.getenv(
        "API_BASE_URL",
        "https://jsonplaceholder.typicode.com",
    )

    # Books to Scrape — public demo site used for UI tests
    UI_BASE_URL: str = os.getenv(
        "UI_BASE_URL",
        "https://books.toscrape.com",
    )

    # ------------------------------------------------------------------ #
    #  Timeouts (seconds)
    # ------------------------------------------------------------------ #

    # Maximum time (s) a single HTTP request is allowed to take
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "15"))

    # Maximum acceptable API response time for performance assertions (ms)
    MAX_RESPONSE_TIME_MS: int = int(os.getenv("MAX_RESPONSE_TIME_MS", "3000"))

    # Playwright page navigation timeout (ms)
    PAGE_TIMEOUT_MS: int = int(os.getenv("PAGE_TIMEOUT_MS", "30000"))

    # ------------------------------------------------------------------ #
    #  Playwright
    # ------------------------------------------------------------------ #

    # Run browser in headless mode by default; set to "false" to watch
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

    # Browser to use: chromium | firefox | webkit
    BROWSER: str = os.getenv("BROWSER", "chromium")

    # ------------------------------------------------------------------ #
    #  Directories
    # ------------------------------------------------------------------ #

    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "reports")
    SCREENSHOTS_DIR: str = os.getenv("SCREENSHOTS_DIR", "screenshots")
    TEST_DATA_PATH: str = os.getenv("TEST_DATA_PATH", "test_data/test_data.json")

    # ------------------------------------------------------------------ #
    #  Logging
    # ------------------------------------------------------------------ #

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Singleton instance — import this everywhere
config = Config()
