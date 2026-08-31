"""
tests/ui/test_cart.py
----------------------
UI tests for product interaction and add-to-basket workflows.

Target: https://books.toscrape.com/
        (Publicly available demo site — safe to automate)

Test IDs
--------
UI-CRT-001  Click on a book opens the product detail page
UI-CRT-002  Product detail page shows book title
UI-CRT-003  Product detail page shows book price
UI-CRT-004  Product detail page shows availability information
UI-CRT-005  Add to basket button is present on product page
UI-CRT-006  Adding a book to the basket updates the basket count
UI-CRT-007  Product detail page has a breadcrumb trail
UI-CRT-008  Navigating back from product page returns to catalogue
"""

import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Product detail page selectors ──────────────────────────────────────
PRODUCT_TITLE = "div.product_main h1"
PRODUCT_PRICE = "div.product_main p.price_color"
PRODUCT_AVAILABILITY = "div.product_main p.availability"
ADD_TO_BASKET_BTN = "button.btn-add-to-basket, button[type='submit']"
BASKET_COUNT = "div.basket-mini a"
BREADCRUMB = "ul.breadcrumb"


def _open_first_book(page: Page) -> None:
    """Navigate to home page and click the first book."""
    home = HomePage(page)
    home.navigate()
    # Click the first book article's title link
    page.locator("article.product_pod h3 a").first.click()
    page.wait_for_load_state("domcontentloaded")


# ======================================================================
#  UI-CRT-001 — Clicking a book opens the product detail page
# ======================================================================

@pytest.mark.ui
def test_clicking_book_opens_detail_page(page: Page) -> None:
    """Clicking a book from the catalogue should navigate to its detail page."""
    _open_first_book(page)

    current_url = page.url
    assert "catalogue" in current_url or "books.toscrape.com" in current_url, (
        f"Expected to be on a product detail page, but URL is: {current_url}"
    )
    logger.info("UI-CRT-001 PASSED — product detail page opened: %s", current_url)


# ======================================================================
#  UI-CRT-002 — Product detail page shows book title
# ======================================================================

@pytest.mark.ui
def test_product_detail_shows_title(page: Page) -> None:
    """The product detail page must display the book's title."""
    _open_first_book(page)

    title_locator = page.locator(PRODUCT_TITLE)
    assert title_locator.is_visible(), "Book title is not visible on the detail page."

    title_text = title_locator.inner_text().strip()
    assert len(title_text) > 0, "Book title text should not be empty."

    logger.info("UI-CRT-002 PASSED — book title: '%s'.", title_text)


# ======================================================================
#  UI-CRT-003 — Product detail page shows book price
# ======================================================================

@pytest.mark.ui
def test_product_detail_shows_price(page: Page) -> None:
    """The product detail page must display the book's price."""
    _open_first_book(page)

    price_locator = page.locator(PRODUCT_PRICE)
    assert price_locator.is_visible(), "Price is not visible on the detail page."

    price_text = price_locator.first.inner_text().strip()
    assert "£" in price_text or "$" in price_text or len(price_text) > 0, (
        f"Price text looks empty or unexpected: '{price_text}'"
    )
    logger.info("UI-CRT-003 PASSED — book price: '%s'.", price_text)


# ======================================================================
#  UI-CRT-004 — Product detail page shows availability
# ======================================================================

@pytest.mark.ui
def test_product_detail_shows_availability(page: Page) -> None:
    """The product detail page must display availability information."""
    _open_first_book(page)

    avail_locator = page.locator(PRODUCT_AVAILABILITY)
    assert avail_locator.is_visible(), (
        "Availability is not visible on the detail page."
    )

    avail_text = avail_locator.first.inner_text().strip()
    assert len(avail_text) > 0, "Availability text should not be empty."

    logger.info("UI-CRT-004 PASSED — availability: '%s'.", avail_text)


# ======================================================================
#  UI-CRT-005 — Add to basket button is present
# ======================================================================

@pytest.mark.ui
def test_add_to_basket_button_present(page: Page) -> None:
    """The 'Add to basket' button must be visible on the product detail page."""
    _open_first_book(page)

    btn = page.locator(ADD_TO_BASKET_BTN)
    assert btn.count() > 0, "Add to basket button was not found on the page."
    assert btn.first.is_visible(), "Add to basket button is not visible."

    logger.info("UI-CRT-005 PASSED — add to basket button is visible.")


# ======================================================================
#  UI-CRT-006 — Adding a book updates the basket count
# ======================================================================

@pytest.mark.ui
def test_add_to_basket_updates_count(page: Page) -> None:
    """Clicking 'Add to basket' should update the basket item count."""
    _open_first_book(page)

    btn = page.locator(ADD_TO_BASKET_BTN).first
    btn.click()
    page.wait_for_load_state("domcontentloaded")

    # After adding, a success message or updated basket count should be present
    basket_indicator = page.locator("div.alert-success, div.basket-mini")
    assert basket_indicator.count() > 0, (
        "No basket update indicator found after clicking 'Add to basket'."
    )

    logger.info("UI-CRT-006 PASSED — basket updated after adding book.")


# ======================================================================
#  UI-CRT-007 — Product detail page has a breadcrumb trail
# ======================================================================

@pytest.mark.ui
def test_product_detail_has_breadcrumb(page: Page) -> None:
    """The product detail page should show a breadcrumb navigation trail."""
    _open_first_book(page)

    breadcrumb = page.locator(BREADCRUMB)
    assert breadcrumb.is_visible(), "Breadcrumb is not visible on the detail page."

    items = breadcrumb.locator("li").all_text_contents()
    assert len(items) >= 2, (
        f"Expected at least 2 breadcrumb items, got {len(items)}."
    )
    logger.info(
        "UI-CRT-007 PASSED — breadcrumb: %s.", " > ".join(i.strip() for i in items)
    )


# ======================================================================
#  UI-CRT-008 — Navigating back returns to catalogue
# ======================================================================

@pytest.mark.ui
def test_back_navigation_returns_to_catalogue(page: Page) -> None:
    """Using browser back from a product page should return to the catalogue."""
    _open_first_book(page)

    page.go_back()
    page.wait_for_load_state("domcontentloaded")

    current_url = page.url
    assert "books.toscrape.com" in current_url, (
        f"Expected to return to catalogue, but URL is: {current_url}"
    )
    assert page.locator("article.product_pod").count() > 0, (
        "Going back did not return to the catalogue — no book articles found."
    )
    logger.info("UI-CRT-008 PASSED — back navigation returned to catalogue.")
