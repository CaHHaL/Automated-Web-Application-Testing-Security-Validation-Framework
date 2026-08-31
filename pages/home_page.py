"""
pages/home_page.py
-------------------
Page Object Model for the Books to Scrape home page.

Encapsulates all selectors and interactions for:
  https://books.toscrape.com/
"""

from playwright.sync_api import Page

from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage:
    """
    Encapsulates browser interactions for the Books to Scrape home page.

    Parameters
    ----------
    page:
        A Playwright ``Page`` instance.
    """

    URL = config.UI_BASE_URL

    # ── Selectors ─────────────────────────────────────────────────────
    LOGO_SELECTOR = "a.navbar-brand"
    BOOK_ARTICLES = "article.product_pod"
    CATEGORY_LINKS = "ul.nav-list ul li a"
    NEXT_BUTTON = "li.next a"
    SEARCH_FORM = "form.form-horizontal"
    BREADCRUMB = "ul.breadcrumb"
    BOOK_TITLES = "article.product_pod h3 a"

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Actions ───────────────────────────────────────────────────────

    def navigate(self) -> None:
        """Open the home page."""
        logger.info("Navigating to home page: %s", self.URL)
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    def get_title(self) -> str:
        """Return the page's <title> text."""
        return self.page.title()

    def get_book_count(self) -> int:
        """Return the number of book articles visible on the page."""
        return self.page.locator(self.BOOK_ARTICLES).count()

    def get_all_category_links(self) -> list:
        """Return a list of all category anchor text values."""
        return self.page.locator(self.CATEGORY_LINKS).all_text_contents()

    def click_category(self, category_name: str) -> None:
        """Click a category link by its visible text."""
        logger.info("Clicking category: '%s'", category_name)
        self.page.locator(self.CATEGORY_LINKS).filter(
            has_text=category_name
        ).first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def is_logo_visible(self) -> bool:
        """Return True if the site logo is visible."""
        return self.page.locator(self.LOGO_SELECTOR).is_visible()

    def has_next_page(self) -> bool:
        """Return True if a 'next' pagination link is present."""
        return self.page.locator(self.NEXT_BUTTON).count() > 0

    def get_book_titles(self) -> list:
        """Return all visible book titles on the current page."""
        return [
            t.strip()
            for t in self.page.locator(self.BOOK_TITLES).all_inner_texts()
        ]

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
