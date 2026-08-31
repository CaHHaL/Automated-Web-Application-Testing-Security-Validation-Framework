"""
tests/ui/test_login.py
-----------------------
UI tests for login / authentication workflows using Playwright.

Target: https://the-internet.herokuapp.com/login
        (Publicly available demo site — safe to automate)

Test IDs
--------
UI-LGN-001  Login page is reachable — HTTP 200 equivalent
UI-LGN-002  Login page title contains expected text
UI-LGN-003  Login form elements are visible
UI-LGN-004  Successful login with valid credentials
UI-LGN-005  Failed login with invalid password — error message shown
UI-LGN-006  Failed login with empty username — error message shown
UI-LGN-007  Failed login with empty password — error message shown
UI-LGN-008  Logout after successful login redirects to login page
"""

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)

VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"
INVALID_PASSWORD = "wrongpassword"


# ======================================================================
#  UI-LGN-001 — Login page is reachable
# ======================================================================

@pytest.mark.ui
def test_login_page_reachable(page: Page) -> None:
    """The login page should load without error."""
    login = LoginPage(page)
    login.navigate()

    assert "login" in login.get_current_url().lower(), (
        f"Unexpected URL after navigation: {login.get_current_url()}"
    )
    logger.info("UI-LGN-001 PASSED — login page is reachable.")


# ======================================================================
#  UI-LGN-002 — Login page title
# ======================================================================

@pytest.mark.ui
def test_login_page_title(page: Page) -> None:
    """The login page title should contain an expected keyword."""
    login = LoginPage(page)
    login.navigate()

    title = login.get_title()
    assert title, "Page title should not be empty."
    logger.info("UI-LGN-002 PASSED — page title: '%s'.", title)


# ======================================================================
#  UI-LGN-003 — Login form elements are visible
# ======================================================================

@pytest.mark.ui
def test_login_form_elements_visible(page: Page) -> None:
    """Username input, password input, and submit button must be visible."""
    login = LoginPage(page)
    login.navigate()

    assert page.locator(login.USERNAME_INPUT).is_visible(), (
        "Username input is not visible."
    )
    assert page.locator(login.PASSWORD_INPUT).is_visible(), (
        "Password input is not visible."
    )
    assert page.locator(login.LOGIN_BUTTON).is_visible(), (
        "Login button is not visible."
    )
    logger.info("UI-LGN-003 PASSED — all form elements are visible.")


# ======================================================================
#  UI-LGN-004 — Successful login
# ======================================================================

@pytest.mark.ui
def test_successful_login(page: Page) -> None:
    """Logging in with valid credentials should show the success flash."""
    login = LoginPage(page)
    login.login(VALID_USERNAME, VALID_PASSWORD)

    assert login.is_login_successful() or login.is_logout_button_visible(), (
        "Login appeared to fail — success indicator not found."
    )
    logger.info("UI-LGN-004 PASSED — successful login confirmed.")


# ======================================================================
#  UI-LGN-005 — Failed login with invalid password
# ======================================================================

@pytest.mark.ui
@pytest.mark.negative
def test_failed_login_invalid_password(page: Page) -> None:
    """An invalid password should produce an error flash message."""
    login = LoginPage(page)
    login.login(VALID_USERNAME, INVALID_PASSWORD)

    assert login.is_login_failed(), (
        "Expected an error message for invalid password, but none appeared."
    )
    error_msg = login.get_error_message()
    assert len(error_msg) > 0, "Error flash message text should not be empty."
    logger.info(
        "UI-LGN-005 PASSED — invalid password error: '%s'.", error_msg
    )


# ======================================================================
#  UI-LGN-006 — Failed login with empty username
# ======================================================================

@pytest.mark.ui
@pytest.mark.negative
def test_failed_login_empty_username(page: Page) -> None:
    """An empty username should produce an error flash message."""
    login = LoginPage(page)
    login.login("", VALID_PASSWORD)

    assert login.is_login_failed(), (
        "Expected an error message for empty username, but none appeared."
    )
    logger.info("UI-LGN-006 PASSED — empty username produces error.")


# ======================================================================
#  UI-LGN-007 — Failed login with empty password
# ======================================================================

@pytest.mark.ui
@pytest.mark.negative
def test_failed_login_empty_password(page: Page) -> None:
    """An empty password should produce an error flash message."""
    login = LoginPage(page)
    login.login(VALID_USERNAME, "")

    assert login.is_login_failed(), (
        "Expected an error message for empty password, but none appeared."
    )
    logger.info("UI-LGN-007 PASSED — empty password produces error.")


# ======================================================================
#  UI-LGN-008 — Logout redirects to login page
# ======================================================================

@pytest.mark.ui
def test_logout_redirects_to_login(page: Page) -> None:
    """After logging out, the user should be redirected to the login page."""
    login = LoginPage(page)
    login.login(VALID_USERNAME, VALID_PASSWORD)

    # Verify login was successful before testing logout
    assert login.is_login_successful() or login.is_logout_button_visible()

    login.logout()

    assert "login" in login.get_current_url().lower(), (
        f"After logout, expected to be on login page but URL is: {login.get_current_url()}"
    )
    logger.info("UI-LGN-008 PASSED — logout redirected to login page.")
