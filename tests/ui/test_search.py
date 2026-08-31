"""
tests/ui/test_search.py
------------------------
UI tests for category navigation and search / browsing workflows.

Target: https://books.toscrape.com/
        (Publicly available demo site — safe to automate)

Test IDs
--------
UI-SRC-001  Home page loads and shows book listings
UI-SRC-002  Home page title contains expected text
UI-SRC-003  Logo is visible on home page
UI-SRC-004  Site shows at least 20 books on the home page
UI-SRC-005  Category links are present in the sidebar
UI-SRC-006  Clicking a category shows books for that category
UI-SRC-007  Breadcrumb updates after category navigation
UI-SRC-008  Pagination next-page link is present on home page
UI-SRC-009  All visible books have non-empty titles
UI-SRC-010  All visible books have price information
"""

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.search_page import SearchPage
from utils.logger import get_logger

logger = get_logger(__name__)


# ======================================================================
#  UI-SRC-001 — Home page loads with book listings
# ======================================================================

@pytest.mark.ui
def test_home_page_loads(page: Page) -> None:
    """The home page should load and display book articles."""
    home = HomePage(page)
    home.navigate()

    assert home.get_book_count() > 0, (
        "Home page should display at least one book."
    )
    logger.info(
        "UI-SRC-001 PASSED — home page shows %d books.", home.get_book_count()
    )


# ======================================================================
#  UI-SRC-002 — Home page title
# ======================================================================

@pytest.mark.ui
def test_home_page_title(page: Page) -> None:
    """Home page title should contain 'Books to Scrape'."""
    home = HomePage(page)
    home.navigate()

    title = home.get_title()
    assert "Books to Scrape" in title or "books" in title.lower(), (
        f"Unexpected page title: '{title}'"
    )
    logger.info("UI-SRC-002 PASSED — page title: '%s'.", title)


# ======================================================================
#  UI-SRC-003 — Logo is visible
# ======================================================================

@pytest.mark.ui
def test_home_page_logo_visible(page: Page) -> None:
    """The site logo should be visible on the home page."""
    home = HomePage(page)
    home.navigate()

    assert home.is_logo_visible(), "Site logo is not visible on the home page."
    logger.info("UI-SRC-003 PASSED — logo is visible.")


# ======================================================================
#  UI-SRC-004 — At least 20 books visible on home page
# ======================================================================

@pytest.mark.ui
def test_home_page_shows_minimum_books(page: Page) -> None:
    """The home page should display at least 20 books (one full page)."""
    home = HomePage(page)
    home.navigate()

    count = home.get_book_count()
    assert count >= 20, (
        f"Expected at least 20 books on home page, got {count}."
    )
    logger.info("UI-SRC-004 PASSED — %d books visible.", count)


# ======================================================================
#  UI-SRC-005 — Category links present in sidebar
# ======================================================================

@pytest.mark.ui
def test_category_links_present(page: Page) -> None:
    """The category sidebar should contain at least 5 category links."""
    home = HomePage(page)
    home.navigate()

    categories = home.get_all_category_links()
    assert len(categories) >= 5, (
        f"Expected at least 5 categories, got {len(categories)}."
    )
    logger.info(
        "UI-SRC-005 PASSED — %d categories found.", len(categories)
    )


# ======================================================================
#  UI-SRC-006 — Clicking a category shows books
# ======================================================================

@pytest.mark.ui
def test_category_navigation_shows_books(page: Page) -> None:
    """Clicking a category should load the category page with books."""
    home = HomePage(page)
    home.navigate()

    home.click_category("Travel")
    search = SearchPage(page)

    assert search.has_results(), (
        "No books found after navigating to the Travel category."
    )
    logger.info(
        "UI-SRC-006 PASSED — Travel category shows %d books.",
        search.get_book_count_on_page(),
    )


# ======================================================================
#  UI-SRC-007 — Breadcrumb updates after category navigation
# ======================================================================

@pytest.mark.ui
def test_breadcrumb_updates_after_category(page: Page) -> None:
    """After navigating to a category, the breadcrumb should reflect it."""
    home = HomePage(page)
    home.navigate()
    home.click_category("Mystery")

    search = SearchPage(page)
    breadcrumb = search.get_current_breadcrumb()

    assert "Mystery" in breadcrumb, (
        f"Expected 'Mystery' in breadcrumb, got: '{breadcrumb}'"
    )
    logger.info("UI-SRC-007 PASSED — breadcrumb shows '%s'.", breadcrumb)


# ======================================================================
#  UI-SRC-008 — Pagination next-page is present
# ======================================================================

@pytest.mark.ui
def test_pagination_next_present(page: Page) -> None:
    """The home page should have a 'next' pagination link (>20 books total)."""
    home = HomePage(page)
    home.navigate()

    assert home.has_next_page(), (
        "Expected a 'next' pagination link on the home page."
    )
    logger.info("UI-SRC-008 PASSED — next page link is present.")


# ======================================================================
#  UI-SRC-009 — All visible books have non-empty titles
# ======================================================================

@pytest.mark.ui
def test_book_titles_not_empty(page: Page) -> None:
    """Every visible book on the home page should have a non-empty title."""
    home = HomePage(page)
    home.navigate()

    titles = home.get_book_titles()
    assert len(titles) > 0, "No book titles found."

    empty_titles = [t for t in titles if not t.strip()]
    assert not empty_titles, (
        f"{len(empty_titles)} book(s) have empty titles."
    )
    logger.info(
        "UI-SRC-009 PASSED — %d books all have non-empty titles.", len(titles)
    )


# ======================================================================
#  UI-SRC-010 — All visible books have price information
# ======================================================================

@pytest.mark.ui
def test_book_prices_present(page: Page) -> None:
    """Every visible book on the home page should show a price."""
    home = HomePage(page)
    home.navigate()

    search = SearchPage(page)
    prices = search.get_book_prices()
    assert len(prices) > 0, "No book prices found."

    empty_prices = [p for p in prices if not p.strip()]
    assert not empty_prices, (
        f"{len(empty_prices)} book(s) have empty price values."
    )
    logger.info(
        "UI-SRC-010 PASSED — %d books all have price information.", len(prices)
    )
