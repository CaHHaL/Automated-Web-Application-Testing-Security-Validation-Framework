"""
tests/api/test_negative.py
--------------------------
Negative API tests — verifying correct behaviour when the application
receives invalid, missing, or unexpected input.

Test IDs
--------
NEG-001  Non-existent user ID → 404
NEG-002  Invalid (non-numeric) user ID → 404 or 4xx
NEG-003  Negative user ID → 404
NEG-004  Zero user ID → 404
NEG-005  Non-existent endpoint → 404
NEG-006  Non-existent post ID → 404
NEG-007  Parameterized invalid user IDs → all return non-200
NEG-008  Very large user ID → 404
NEG-009  POST with missing required fields — no server crash
NEG-010  DELETE on non-existent resource — graceful response
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)


# ======================================================================
#  NEG-001 — Non-existent user ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_nonexistent_user(api_client: APIClient) -> None:
    """GET /users/999999 should return HTTP 404."""
    response = api_client.get("/users/999999")

    assert response.status_code == 404, (
        f"Expected 404 for non-existent user, got {response.status_code}"
    )
    logger.info("NEG-001 PASSED — /users/999999 returned 404.")


# ======================================================================
#  NEG-002 — Non-numeric user ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_user_with_string_id(api_client: APIClient) -> None:
    """GET /users/abc should return a 4xx error (not 200)."""
    response = api_client.get("/users/abc")

    assert response.status_code in (400, 404), (
        f"Expected 4xx for string user ID, got {response.status_code}"
    )
    logger.info(
        "NEG-002 PASSED — /users/abc returned %d.", response.status_code
    )


# ======================================================================
#  NEG-003 — Negative user ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_user_with_negative_id(api_client: APIClient) -> None:
    """GET /users/-1 should return HTTP 404."""
    response = api_client.get("/users/-1")

    assert response.status_code == 404, (
        f"Expected 404 for negative user ID, got {response.status_code}"
    )
    logger.info("NEG-003 PASSED — /users/-1 returned 404.")


# ======================================================================
#  NEG-004 — Zero user ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_user_with_zero_id(api_client: APIClient) -> None:
    """GET /users/0 should return HTTP 404."""
    response = api_client.get("/users/0")

    assert response.status_code == 404, (
        f"Expected 404 for user ID 0, got {response.status_code}"
    )
    logger.info("NEG-004 PASSED — /users/0 returned 404.")


# ======================================================================
#  NEG-005 — Non-existent endpoint
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_nonexistent_endpoint(api_client: APIClient) -> None:
    """GET /nonexistent should return HTTP 404."""
    response = api_client.get("/nonexistent")

    assert response.status_code == 404, (
        f"Expected 404 for unknown endpoint, got {response.status_code}"
    )
    logger.info("NEG-005 PASSED — /nonexistent returned 404.")


# ======================================================================
#  NEG-006 — Non-existent post ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_nonexistent_post(api_client: APIClient) -> None:
    """GET /posts/999999 should return HTTP 404."""
    response = api_client.get("/posts/999999")

    assert response.status_code == 404, (
        f"Expected 404 for non-existent post, got {response.status_code}"
    )
    logger.info("NEG-006 PASSED — /posts/999999 returned 404.")


# ======================================================================
#  NEG-007 — Parameterized invalid user IDs
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize("user_id", [0, -1, 999999, 9999999])
def test_invalid_user_ids_parameterized(
    api_client: APIClient, user_id: int
) -> None:
    """Invalid user IDs should all produce a non-200 response."""
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code != 200, (
        f"Expected non-200 for user_id={user_id}, got {response.status_code}"
    )
    logger.info(
        "NEG-007 PASSED — /users/%s returned %d.",
        user_id,
        response.status_code,
    )


# ======================================================================
#  NEG-008 — Very large user ID
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_get_user_with_very_large_id(api_client: APIClient) -> None:
    """GET /users/2147483647 (INT_MAX) should return 404."""
    response = api_client.get("/users/2147483647")

    assert response.status_code == 404, (
        f"Expected 404 for INT_MAX user ID, got {response.status_code}"
    )
    logger.info("NEG-008 PASSED — /users/2147483647 returned 404.")


# ======================================================================
#  NEG-009 — POST with missing required fields
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_post_with_missing_fields(api_client: APIClient) -> None:
    """
    POST /posts with an empty body should not crash the server.
    JSONPlaceholder returns 201 for any POST (it is a mock), so we
    verify that the server handles it gracefully — not a 5xx error.
    """
    response = api_client.post("/posts", json={})

    assert response.status_code < 500, (
        f"Server returned 5xx for empty POST body: {response.status_code}"
    )
    logger.info(
        "NEG-009 PASSED — POST /posts with empty body returned %d.",
        response.status_code,
    )


# ======================================================================
#  NEG-010 — DELETE on non-existent resource
# ======================================================================

@pytest.mark.api
@pytest.mark.negative
def test_delete_nonexistent_post(api_client: APIClient) -> None:
    """
    DELETE /posts/999999 should not crash the server (no 5xx error).
    JSONPlaceholder returns 200 for any DELETE, so we accept 2xx or 4xx.
    """
    response = api_client.delete("/posts/999999")

    assert response.status_code < 500, (
        f"Server returned 5xx for DELETE on non-existent post: {response.status_code}"
    )
    logger.info(
        "NEG-010 PASSED — DELETE /posts/999999 returned %d.",
        response.status_code,
    )
