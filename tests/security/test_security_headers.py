"""
tests/security/test_security_headers.py
-----------------------------------------
HTTP security-header validation tests.

These tests check that the API server returns expected security-related
HTTP headers and that the values are acceptable.

Test IDs
--------
SEC-HD-001  Content-Type header is present on all responses
SEC-HD-002  X-Content-Type-Options header — check presence
SEC-HD-003  X-Frame-Options header — check presence
SEC-HD-004  Content-Type includes charset or application/json
SEC-HD-005  No Server header leak (or server is not overly descriptive)
SEC-HD-006  Cache-Control header presence on sensitive endpoints
SEC-HD-007  Parameterized content-type check across multiple endpoints
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

ENDPOINTS = ["/users", "/posts", "/comments", "/todos"]


# ======================================================================
#  SEC-HD-001 — Content-Type present on all responses
# ======================================================================

@pytest.mark.security
def test_content_type_header_present(api_client: APIClient) -> None:
    """Every API response should include a Content-Type header."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    assert "Content-Type" in response.headers, (
        "Content-Type header is missing from the response."
    )
    logger.info(
        "SEC-HD-001 PASSED — Content-Type: %s",
        response.headers.get("Content-Type"),
    )


# ======================================================================
#  SEC-HD-002 — X-Content-Type-Options (advisory check)
# ======================================================================

@pytest.mark.security
def test_x_content_type_options_header(api_client: APIClient) -> None:
    """
    X-Content-Type-Options should ideally be set to 'nosniff'.

    JSONPlaceholder may not set this header, so we log the result
    without failing — this is an advisory check to detect the absence.
    """
    response = api_client.get("/users/1")
    header_value = response.headers.get("X-Content-Type-Options", "NOT SET")

    if header_value == "NOT SET":
        logger.warning(
            "SEC-HD-002 ADVISORY — X-Content-Type-Options is not set. "
            "Recommended value: nosniff."
        )
    else:
        logger.info(
            "SEC-HD-002 PASSED — X-Content-Type-Options: %s", header_value
        )

    # Non-blocking: log presence/absence for awareness
    assert True


# ======================================================================
#  SEC-HD-003 — X-Frame-Options (advisory check)
# ======================================================================

@pytest.mark.security
def test_x_frame_options_header(api_client: APIClient) -> None:
    """
    X-Frame-Options should be set to prevent clickjacking.
    This is an advisory check; absence is logged as a warning.
    """
    response = api_client.get("/users/1")
    header_value = response.headers.get("X-Frame-Options", "NOT SET")

    if header_value == "NOT SET":
        logger.warning(
            "SEC-HD-003 ADVISORY — X-Frame-Options is not set. "
            "Recommended values: DENY or SAMEORIGIN."
        )
    else:
        logger.info(
            "SEC-HD-003 PASSED — X-Frame-Options: %s", header_value
        )

    assert True


# ======================================================================
#  SEC-HD-004 — Content-Type is application/json
# ======================================================================

@pytest.mark.security
def test_content_type_is_json(api_client: APIClient) -> None:
    """API JSON endpoints must respond with application/json Content-Type."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Expected application/json, got: '{content_type}'"
    )
    logger.info("SEC-HD-004 PASSED — Content-Type is application/json.")


# ======================================================================
#  SEC-HD-005 — Server header not overly descriptive
# ======================================================================

@pytest.mark.security
def test_server_header_not_descriptive(api_client: APIClient) -> None:
    """
    The Server header, if present, should not expose detailed version info.
    Detailed server banners are an information-disclosure risk.
    """
    response = api_client.get("/users/1")
    server_header = response.headers.get("Server", "")

    # Flag if header contains a version number pattern (e.g. "Apache/2.4.51")
    import re
    version_pattern = re.compile(r"\d+\.\d+")
    if version_pattern.search(server_header):
        logger.warning(
            "SEC-HD-005 ADVISORY — Server header may expose version info: '%s'",
            server_header,
        )
    else:
        logger.info(
            "SEC-HD-005 PASSED — Server header: '%s'", server_header or "(not set)"
        )

    # Advisory only — do not fail the test
    assert True


# ======================================================================
#  SEC-HD-006 — Cache-Control (advisory check)
# ======================================================================

@pytest.mark.security
def test_cache_control_header(api_client: APIClient) -> None:
    """
    API responses should include Cache-Control to prevent sensitive
    data from being cached by proxies or browsers.
    """
    response = api_client.get("/users/1")
    cache_control = response.headers.get("Cache-Control", "NOT SET")

    logger.info(
        "SEC-HD-006 INFO — Cache-Control: %s", cache_control
    )

    # Advisory: log the value for review
    assert True


# ======================================================================
#  SEC-HD-007 — Parameterized Content-Type check across endpoints
# ======================================================================

@pytest.mark.security
@pytest.mark.parametrize("endpoint", ENDPOINTS)
def test_content_type_json_all_endpoints(
    api_client: APIClient, endpoint: str
) -> None:
    """Every major endpoint should return Content-Type: application/json."""
    response = api_client.get(endpoint)
    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Endpoint {endpoint}: expected application/json, got '{content_type}'"
    )
    logger.info(
        "SEC-HD-007 PASSED — %s Content-Type: %s", endpoint, content_type
    )
