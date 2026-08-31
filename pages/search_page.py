"""
pages/search_page.py
---------------------
Page Object Model for the Books to Scrape category / search results page.

Encapsulates all selectors and interactions for category pages and
book listing pages on https://books.toscrape.com/
"""

from playwright.sync_api import Page

from utils.logger import get_logger

logger = get_logger(__name__)


class SearchPage:
    """
    Encapsulates browser interactions for the Books to Scrape category
    and search results pages.

    Parameters
    ----------
    page:
        A Playwright ``Page`` instance.
    """

    # ── Selectors ─────────────────────────────────────────────────────
    BOOK_ARTICLES = "article.product_pod"
    BOOK_TITLES = "article.product_pod h3 a"
    BOOK_PRICES = "article.product_pod p.price_color"
    BOOK_RATINGS = "article.product_pod p.star-rating"
    RESULT_COUNT = "form.form-horizontal strong:first-child"
    BREADCRUMB = "ul.breadcrumb li:last-child"
    PAGINATION_NEXT = "li.next a"
    PAGINATION_PREV = "li.previous a"
    BOOK_AVAILABILITY = "article.product_pod p.availability"

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Queries ───────────────────────────────────────────────────────

    def get_book_count_on_page(self) -> int:
        """Return the number of book result cards on the current page."""
        return self.page.locator(self.BOOK_ARTICLES).count()

    def get_book_titles(self) -> list:
        """Return all book title strings visible on the page."""
        return [
            t.strip()
            for t in self.page.locator(self.BOOK_TITLES).all_inner_texts()
        ]

    def get_book_prices(self) -> list:
        """Return all book price strings visible on the page."""
        return self.page.locator(self.BOOK_PRICES).all_text_contents()

    def get_current_breadcrumb(self) -> str:
        """Return the text of the deepest breadcrumb item."""
        locator = self.page.locator(self.BREADCRUMB)
        if locator.count() > 0:
            return locator.first.inner_text().strip()
        return ""

    def has_results(self) -> bool:
        """Return True if at least one book result is visible."""
        return self.get_book_count_on_page() > 0

    def has_next_page(self) -> bool:
        """Return True if a 'next' pagination link is present."""
        return self.page.locator(self.PAGINATION_NEXT).count() > 0

    def click_next_page(self) -> None:
        """Click the 'next' pagination link."""
        self.page.locator(self.PAGINATION_NEXT).first.click()
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Navigated to next page.")

    def click_book_by_index(self, index: int = 0) -> None:
        """
        Click on a book article by its index on the page.

        Parameters
        ----------
        index:
            Zero-based index of the book to click. Defaults to the first.
        """
        self.page.locator(self.BOOK_ARTICLES).nth(index).click()
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Clicked book at index %d.", index)

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
