"""
utils/api_client.py
-------------------
Reusable HTTP client that wraps the ``requests`` library.

All tests use this client instead of calling ``requests`` directly so
that cross-cutting concerns (timeouts, logging, base-URL composition,
future auth) are handled in one place.

Usage
-----
    from utils.api_client import APIClient

    client = APIClient()
    response = client.get("/users/1")
    assert response.status_code == 200
"""

import time
from typing import Any, Dict, Optional

import requests
from requests import Response

from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    """
    Thread-safe HTTP client with logging and base-URL support.

    Parameters
    ----------
    base_url:
        Root URL prepended to every relative path.  Defaults to the
        value in ``Config.API_BASE_URL``.
    timeout:
        Per-request timeout in seconds.  Defaults to ``Config.REQUEST_TIMEOUT``.
    """

    def __init__(
        self,
        base_url: str = config.API_BASE_URL,
        timeout: int = config.REQUEST_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _build_url(self, path: str) -> str:
        """Compose the full URL from a relative path."""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Response:
        """
        Execute an HTTP request and log the outcome.

        Parameters
        ----------
        method:
            HTTP verb — ``GET``, ``POST``, ``PUT``, ``PATCH``, ``DELETE``.
        path:
            Relative path or full URL.
        **kwargs:
            Forwarded directly to ``requests.Session.request``.

        Returns
        -------
        requests.Response
        """
        url = self._build_url(path)
        kwargs.setdefault("timeout", self.timeout)

        logger.info("→ %s  %s", method.upper(), url)
        if kwargs.get("json"):
            logger.debug("   Body: %s", kwargs["json"])
        if kwargs.get("params"):
            logger.debug("   Params: %s", kwargs["params"])

        start = time.perf_counter()
        response = self.session.request(method, url, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "← %s  %s  (%.0f ms)",
            response.status_code,
            url,
            elapsed_ms,
        )
        if not response.ok:
            logger.warning("   Response body: %s", response.text[:500])

        return response

    # ------------------------------------------------------------------ #
    #  Public methods
    # ------------------------------------------------------------------ #

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a GET request."""
        return self._request("GET", path, params=params, **kwargs)

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a POST request with a JSON body."""
        return self._request("POST", path, json=json, **kwargs)

    def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a PUT request with a JSON body."""
        return self._request("PUT", path, json=json, **kwargs)

    def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Response:
        """Send a PATCH request with a JSON body."""
        return self._request("PATCH", path, json=json, **kwargs)

    def delete(
        self,
        path: str,
        **kwargs: Any,
    ) -> Response:
        """Send a DELETE request."""
        return self._request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the underlying session and release resources."""
        self.session.close()
        logger.debug("APIClient session closed.")

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
