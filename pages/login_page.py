"""
pages/login_page.py
--------------------
Page Object Model for authentication-style pages.

Books to Scrape does not require authentication, so this page object
is modelled on a generic login page pattern for demonstration purposes.
It can be pointed at any application that has a login form.
"""

from playwright.sync_api import Page

from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage:
    """
    Generic login page POM — demonstrates the Page Object Model pattern.

    Selectors are written for a typical username/password login form.
    Update ``URL`` and the selectors for a real application target.

    Parameters
    ----------
    page:
        A Playwright ``Page`` instance.
    """

    URL = "https://the-internet.herokuapp.com/login"

    # ── Selectors ─────────────────────────────────────────────────────
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    SUCCESS_FLASH = ".flash.success"
    ERROR_FLASH = ".flash.error"
    LOGOUT_BUTTON = "a[href='/logout']"

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Actions ───────────────────────────────────────────────────────

    def navigate(self) -> None:
        """Open the login page."""
        logger.info("Navigating to login page: %s", self.URL)
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    def enter_username(self, username: str) -> None:
        """Type a username into the username field."""
        self.page.fill(self.USERNAME_INPUT, username)
        logger.debug("Entered username: '%s'", username)

    def enter_password(self, password: str) -> None:
        """Type a password into the password field."""
        self.page.fill(self.PASSWORD_INPUT, password)
        logger.debug("Entered password.")

    def click_login(self) -> None:
        """Click the login submit button."""
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Login button clicked.")

    def login(self, username: str, password: str) -> None:
        """
        Complete the login workflow in one call.

        Parameters
        ----------
        username:
            The username to enter.
        password:
            The password to enter.
        """
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertions / Queries ──────────────────────────────────────────

    def is_login_successful(self) -> bool:
        """Return True if the success flash message is visible."""
        return self.page.locator(self.SUCCESS_FLASH).count() > 0

    def is_login_failed(self) -> bool:
        """Return True if the error flash message is visible."""
        return self.page.locator(self.ERROR_FLASH).count() > 0

    def get_error_message(self) -> str:
        """Return the text of the error flash message."""
        locator = self.page.locator(self.ERROR_FLASH)
        if locator.count() > 0:
            return locator.first.inner_text().strip()
        return ""

    def is_logout_button_visible(self) -> bool:
        """Return True if the logout button is visible (user is logged in)."""
        return self.page.locator(self.LOGOUT_BUTTON).is_visible()

    def logout(self) -> None:
        """Click the logout button."""
        self.page.click(self.LOGOUT_BUTTON)
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Logout button clicked.")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the page's <title> text."""
        return self.page.title()
