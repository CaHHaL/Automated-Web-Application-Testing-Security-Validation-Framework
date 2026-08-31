"""
tests/security/test_input_validation.py
----------------------------------------
Security-oriented input validation tests.

These tests verify that the application handles security-sensitive
and malformed inputs gracefully — without crashing, leaking stack
traces, or returning unexpected 5xx errors.

IMPORTANT: Only run these tests against applications you own or are
           explicitly authorized to test.

Test IDs
--------
SEC-IV-001  XSS payload in post title — no 5xx response
SEC-IV-002  SQL injection in post body — no 5xx response
SEC-IV-003  XSS payload as URL path segment — no 5xx response
SEC-IV-004  Oversized input — no 5xx response
SEC-IV-005  Null-byte injection — no 5xx response
SEC-IV-006  Special characters in query parameter — no 5xx response
SEC-IV-007  Path traversal attempt — no 5xx response
SEC-IV-008  Parameterized XSS payloads via POST body
SEC-IV-009  Parameterized SQL injection payloads via POST body
SEC-IV-010  Empty string values in POST body — no 5xx response
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

XSS_PAYLOADS = [
    "<script>alert('xss')</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "javascript:alert(document.cookie)",
]

SQL_PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE posts; --",
    "1' OR '1' = '1' /*",
    "admin'--",
]


# ======================================================================
#  SEC-IV-001 — XSS payload in post title (POST body)
# ======================================================================

@pytest.mark.security
def test_xss_in_post_title(api_client: APIClient) -> None:
    """Submitting an XSS payload in the title field should not cause a 5xx error."""
    payload = {
        "title": "<script>alert('xss')</script>",
        "body": "Security test from WebTestX.",
        "userId": 1,
    }
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for XSS payload in title: {response.status_code}"
    )
    logger.info(
        "SEC-IV-001 PASSED — XSS in title returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-002 — SQL injection in post body (POST body)
# ======================================================================

@pytest.mark.security
def test_sql_injection_in_post_body(api_client: APIClient) -> None:
    """Submitting an SQL injection string in the body should not cause a 5xx error."""
    payload = {
        "title": "Security Test",
        "body": "'; DROP TABLE posts; --",
        "userId": 1,
    }
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for SQL injection payload: {response.status_code}"
    )
    logger.info(
        "SEC-IV-002 PASSED — SQL injection in body returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-003 — XSS payload as URL path segment
# ======================================================================

@pytest.mark.security
def test_xss_in_url_path(api_client: APIClient) -> None:
    """An XSS payload in the URL path should not cause a 5xx error."""
    response = api_client.get("/posts/%3Cscript%3Ealert(1)%3C/script%3E")

    assert response.status_code < 500, (
        f"Server returned 5xx for XSS URL path: {response.status_code}"
    )
    logger.info(
        "SEC-IV-003 PASSED — XSS URL path returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-004 — Oversized input in POST body
# ======================================================================

@pytest.mark.security
def test_oversized_input_in_post_body(api_client: APIClient) -> None:
    """An extremely large input string in the body should not cause a 5xx error."""
    oversized = "A" * 100_000  # 100 KB
    payload = {
        "title": "Oversized Input Test",
        "body": oversized,
        "userId": 1,
    }
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for oversized input: {response.status_code}"
    )
    logger.info(
        "SEC-IV-004 PASSED — oversized input returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-005 — Null-byte injection
# ======================================================================

@pytest.mark.security
def test_null_byte_in_post_title(api_client: APIClient) -> None:
    """A null-byte character in the title should not cause a 5xx error."""
    payload = {
        "title": "Normal title\x00injected",
        "body": "Null-byte test.",
        "userId": 1,
    }
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for null-byte payload: {response.status_code}"
    )
    logger.info(
        "SEC-IV-005 PASSED — null-byte payload returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-006 — Special characters in query parameter
# ======================================================================

@pytest.mark.security
def test_special_chars_in_query_param(api_client: APIClient) -> None:
    """Special characters in a query param should not cause a 5xx error."""
    response = api_client.get(
        "/posts", params={"userId": "!@#$%^&*()_+"}
    )

    assert response.status_code < 500, (
        f"Server returned 5xx for special-char query param: {response.status_code}"
    )
    logger.info(
        "SEC-IV-006 PASSED — special chars in query returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-007 — Path traversal attempt
# ======================================================================

@pytest.mark.security
def test_path_traversal_attempt(api_client: APIClient) -> None:
    """A path traversal string in the URL should not cause a 5xx error."""
    response = api_client.get("/posts/../../etc/passwd")

    assert response.status_code < 500, (
        f"Server returned 5xx for path traversal: {response.status_code}"
    )
    logger.info(
        "SEC-IV-007 PASSED — path traversal returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-008 — Parameterized XSS payloads via POST body
# ======================================================================

@pytest.mark.security
@pytest.mark.parametrize("xss_payload", XSS_PAYLOADS)
def test_xss_payloads_parameterized(api_client: APIClient, xss_payload: str) -> None:
    """Each XSS payload submitted in a POST body should not cause a 5xx error."""
    payload = {"title": xss_payload, "body": "XSS test", "userId": 1}
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for XSS payload '{xss_payload[:40]}': {response.status_code}"
    )
    logger.info(
        "SEC-IV-008 PASSED — XSS payload returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-009 — Parameterized SQL injection payloads via POST body
# ======================================================================

@pytest.mark.security
@pytest.mark.parametrize("sql_payload", SQL_PAYLOADS)
def test_sql_injection_payloads_parameterized(
    api_client: APIClient, sql_payload: str
) -> None:
    """Each SQL injection payload submitted in a POST body should not cause a 5xx error."""
    payload = {"title": "SQL Test", "body": sql_payload, "userId": 1}
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for SQL payload '{sql_payload[:40]}': {response.status_code}"
    )
    logger.info(
        "SEC-IV-009 PASSED — SQL injection payload returned %d.", response.status_code
    )


# ======================================================================
#  SEC-IV-010 — Empty string values in POST body
# ======================================================================

@pytest.mark.security
def test_empty_string_values_in_post(api_client: APIClient) -> None:
    """Empty string values in all POST body fields should not cause a 5xx error."""
    payload = {"title": "", "body": "", "userId": 1}
    response = api_client.post("/posts", json=payload)

    assert response.status_code < 500, (
        f"Server returned 5xx for empty string POST: {response.status_code}"
    )
    logger.info(
        "SEC-IV-010 PASSED — empty string values returned %d.", response.status_code
    )
