"""
tests/security/test_parameter_handling.py
------------------------------------------
Parameter handling security tests — verifying that the application
correctly validates, rejects, or gracefully handles unusual, malformed,
or unexpected query and path parameters.

Test IDs
--------
SEC-PH-001  Unexpected extra query parameter — ignored or handled gracefully
SEC-PH-002  Boolean value as a numeric parameter — no 5xx
SEC-PH-003  Float value as a user ID — no 5xx
SEC-PH-004  Very large numeric parameter — no 5xx
SEC-PH-005  Array as a query parameter — no 5xx
SEC-PH-006  Unicode characters in parameter — no 5xx
SEC-PH-007  Hex-encoded characters in path — no 5xx
SEC-PH-008  Parameterized invalid param types for userId filter
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

INVALID_USER_ID_TYPES = ["true", "null", "undefined", "NaN", "[]", "{}", "''"]


# ======================================================================
#  SEC-PH-001 — Unexpected extra query parameter
# ======================================================================

@pytest.mark.security
def test_extra_query_parameter_ignored(api_client: APIClient) -> None:
    """Unexpected extra query parameters should be ignored — not cause a 5xx."""
    response = api_client.get(
        "/users/1", params={"__injection__": "value", "extra": "param"}
    )

    assert response.status_code < 500, (
        f"Server returned 5xx for extra query params: {response.status_code}"
    )
    logger.info(
        "SEC-PH-001 PASSED — extra query params returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-002 — Boolean as numeric parameter
# ======================================================================

@pytest.mark.security
def test_boolean_as_user_id(api_client: APIClient) -> None:
    """Passing 'true' as a user ID should not cause a 5xx error."""
    response = api_client.get("/users/true")

    assert response.status_code < 500, (
        f"Server returned 5xx for boolean user ID: {response.status_code}"
    )
    logger.info(
        "SEC-PH-002 PASSED — /users/true returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-003 — Float value as user ID
# ======================================================================

@pytest.mark.security
def test_float_as_user_id(api_client: APIClient) -> None:
    """Passing '1.5' as a user ID should not cause a 5xx error."""
    response = api_client.get("/users/1.5")

    assert response.status_code < 500, (
        f"Server returned 5xx for float user ID: {response.status_code}"
    )
    logger.info(
        "SEC-PH-003 PASSED — /users/1.5 returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-004 — Very large numeric parameter
# ======================================================================

@pytest.mark.security
def test_very_large_numeric_param(api_client: APIClient) -> None:
    """A very large integer as a user ID should not cause a 5xx error."""
    response = api_client.get("/users/99999999999999999999")

    assert response.status_code < 500, (
        f"Server returned 5xx for very large ID: {response.status_code}"
    )
    logger.info(
        "SEC-PH-004 PASSED — very large ID returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-005 — Array as a query parameter
# ======================================================================

@pytest.mark.security
def test_array_as_query_param(api_client: APIClient) -> None:
    """Passing an array-like value as userId query param should not cause 5xx."""
    response = api_client.get("/posts", params={"userId": "[1,2,3]"})

    assert response.status_code < 500, (
        f"Server returned 5xx for array-like query param: {response.status_code}"
    )
    logger.info(
        "SEC-PH-005 PASSED — array-like query param returned %d.",
        response.status_code,
    )


# ======================================================================
#  SEC-PH-006 — Unicode characters in parameter
# ======================================================================

@pytest.mark.security
def test_unicode_in_query_param(api_client: APIClient) -> None:
    """Unicode characters in a query parameter should not cause a 5xx error."""
    response = api_client.get("/posts", params={"title": "テスト 测试 тест"})

    assert response.status_code < 500, (
        f"Server returned 5xx for Unicode query param: {response.status_code}"
    )
    logger.info(
        "SEC-PH-006 PASSED — Unicode query param returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-007 — Hex-encoded path characters
# ======================================================================

@pytest.mark.security
def test_hex_encoded_path(api_client: APIClient) -> None:
    """Hex-encoded path characters should not cause a 5xx error."""
    # %2F = '/', %3B = ';', %27 = '\''
    response = api_client.get("/posts/%2F%3B%27")

    assert response.status_code < 500, (
        f"Server returned 5xx for hex-encoded path: {response.status_code}"
    )
    logger.info(
        "SEC-PH-007 PASSED — hex-encoded path returned %d.", response.status_code
    )


# ======================================================================
#  SEC-PH-008 — Parameterized invalid param types for userId filter
# ======================================================================

@pytest.mark.security
@pytest.mark.parametrize("invalid_user_id", INVALID_USER_ID_TYPES)
def test_invalid_userid_filter_types(
    api_client: APIClient, invalid_user_id: str
) -> None:
    """Filtering posts with an invalid userId type should not cause a 5xx."""
    response = api_client.get("/posts", params={"userId": invalid_user_id})

    assert response.status_code < 500, (
        f"Server returned 5xx for userId='{invalid_user_id}': {response.status_code}"
    )
    logger.info(
        "SEC-PH-008 PASSED — userId='%s' returned %d.",
        invalid_user_id,
        response.status_code,
    )
