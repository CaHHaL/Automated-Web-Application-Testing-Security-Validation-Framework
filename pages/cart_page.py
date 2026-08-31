"""
pages/cart_page.py
-------------------
Page Object Model for the Books to Scrape basket / cart page.

Encapsulates all selectors and interactions for the basket checkout
flow on https://books.toscrape.com/
"""

from playwright.sync_api import Page

from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage:
    """
    Encapsulates browser interactions for the basket page.

    Parameters
    ----------
    page:
        A Playwright ``Page`` instance.
    """

    URL = "https://books.toscrape.com/basket/"

    # ── Selectors ─────────────────────────────────────────────────────
    BASKET_ITEMS = "table#basket_formset tr.basket-items"
    BASKET_TOTAL = "p.basket-mini__headline a"
    EMPTY_BASKET_MSG = "div.content p"
    REMOVE_BUTTONS = "button[data-behaviours='remove']"
    CHECKOUT_BUTTON = "a.btn-lg[href*='checkout']"
    ITEM_TITLES = "td.basket-items__desc h3"
    ITEM_PRICES = "td.basket-items__price p.price_color"
    MINI_BASKET = "div.basket-mini"

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Actions ───────────────────────────────────────────────────────

    def navigate(self) -> None:
        """Open the basket page directly."""
        logger.info("Navigating to basket page: %s", self.URL)
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    # ── Queries ───────────────────────────────────────────────────────

    def get_item_count(self) -> int:
        """Return the number of line items in the basket."""
        return self.page.locator(self.BASKET_ITEMS).count()

    def is_basket_empty(self) -> bool:
        """Return True if the basket is empty."""
        return self.get_item_count() == 0

    def get_item_titles(self) -> list:
        """Return the title text of all items in the basket."""
        locator = self.page.locator(self.ITEM_TITLES)
        if locator.count() == 0:
            return []
        return [t.strip() for t in locator.all_inner_texts()]

    def get_item_prices(self) -> list:
        """Return the price text of all items in the basket."""
        locator = self.page.locator(self.ITEM_PRICES)
        if locator.count() == 0:
            return []
        return [p.strip() for p in locator.all_text_contents()]

    def is_checkout_button_visible(self) -> bool:
        """Return True if the proceed-to-checkout button is visible."""
        btn = self.page.locator(self.CHECKOUT_BUTTON)
        return btn.count() > 0 and btn.first.is_visible()

    def remove_first_item(self) -> None:
        """Click the remove button for the first basket item."""
        remove_btn = self.page.locator(self.REMOVE_BUTTONS).first
        if remove_btn.is_visible():
            remove_btn.click()
            self.page.wait_for_load_state("domcontentloaded")
            logger.info("Removed first item from basket.")

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
