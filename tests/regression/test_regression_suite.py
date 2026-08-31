"""
tests/regression/test_regression_suite.py
------------------------------------------
Core regression suite — re-runs critical existing tests after any
application change to verify that known-good behaviours still hold.

These tests are the safety net: if any of these fail after a change,
the change has broken existing functionality.

Test IDs
--------
REG-001  Users endpoint is reachable and returns 200
REG-002  Posts endpoint is reachable and returns 200
REG-003  Comments endpoint is reachable and returns 200
REG-004  Todos endpoint is reachable and returns 200
REG-005  Albums endpoint is reachable and returns 200
REG-006  Photos endpoint is reachable and returns 200
REG-007  User count has not changed (JSONPlaceholder always returns 10)
REG-008  Post count has not changed (JSONPlaceholder always returns 100)
REG-009  Todo count has not changed (JSONPlaceholder always returns 200)
REG-010  Known user fields remain present (regression on API contract)
REG-011  Known post fields remain present
REG-012  Non-existent user still returns 404 (negative regression)
REG-013  Non-existent post still returns 404 (negative regression)
REG-014  User-to-posts relationship is intact
REG-015  Post-to-comments relationship is intact
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Known stable counts from JSONPlaceholder ──────────────────────────
EXPECTED_USER_COUNT = 10
EXPECTED_POST_COUNT = 100
EXPECTED_TODO_COUNT = 200

REQUIRED_USER_FIELDS = ["id", "name", "username", "email", "address", "phone", "website", "company"]
REQUIRED_POST_FIELDS = ["id", "userId", "title", "body"]


# ======================================================================
#  REG-001 to REG-006 — Core endpoints reachable
# ======================================================================

@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.parametrize("endpoint", [
    "/users",
    "/posts",
    "/comments",
    "/todos",
    "/albums",
    "/photos",
])
def test_core_endpoints_return_200(
    api_client: APIClient, endpoint: str
) -> None:
    """Every core endpoint must return HTTP 200 after any change."""
    response = api_client.get(endpoint)

    assert response.status_code == 200, (
        f"REGRESSION: {endpoint} returned {response.status_code} — expected 200."
    )
    data = response.json()
    assert isinstance(data, list) and len(data) > 0, (
        f"REGRESSION: {endpoint} returned empty or non-list response."
    )
    logger.info("Regression PASSED — %s returned 200.", endpoint)


# ======================================================================
#  REG-007 — User count regression
# ======================================================================

@pytest.mark.regression
def test_user_count_unchanged(api_client: APIClient) -> None:
    """The number of users must still be exactly 10."""
    response = api_client.get("/users")
    assert response.status_code == 200

    count = len(response.json())
    assert count == EXPECTED_USER_COUNT, (
        f"REGRESSION: User count changed — expected {EXPECTED_USER_COUNT}, got {count}."
    )
    logger.info("REG-007 PASSED — user count = %d.", count)


# ======================================================================
#  REG-008 — Post count regression
# ======================================================================

@pytest.mark.regression
def test_post_count_unchanged(api_client: APIClient) -> None:
    """The number of posts must still be exactly 100."""
    response = api_client.get("/posts")
    assert response.status_code == 200

    count = len(response.json())
    assert count == EXPECTED_POST_COUNT, (
        f"REGRESSION: Post count changed — expected {EXPECTED_POST_COUNT}, got {count}."
    )
    logger.info("REG-008 PASSED — post count = %d.", count)


# ======================================================================
#  REG-009 — Todo count regression
# ======================================================================

@pytest.mark.regression
def test_todo_count_unchanged(api_client: APIClient) -> None:
    """The number of todos must still be exactly 200."""
    response = api_client.get("/todos")
    assert response.status_code == 200

    count = len(response.json())
    assert count == EXPECTED_TODO_COUNT, (
        f"REGRESSION: Todo count changed — expected {EXPECTED_TODO_COUNT}, got {count}."
    )
    logger.info("REG-009 PASSED — todo count = %d.", count)


# ======================================================================
#  REG-010 — User API contract regression
# ======================================================================

@pytest.mark.regression
def test_user_api_contract_unchanged(api_client: APIClient) -> None:
    """All required user fields must still be present after any change."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    user = response.json()
    missing = [f for f in REQUIRED_USER_FIELDS if f not in user]
    assert not missing, (
        f"REGRESSION: User API contract broken — missing fields: {missing}"
    )
    logger.info("REG-010 PASSED — user API contract is intact.")


# ======================================================================
#  REG-011 — Post API contract regression
# ======================================================================

@pytest.mark.regression
def test_post_api_contract_unchanged(api_client: APIClient) -> None:
    """All required post fields must still be present after any change."""
    response = api_client.get("/posts/1")
    assert response.status_code == 200

    post = response.json()
    missing = [f for f in REQUIRED_POST_FIELDS if f not in post]
    assert not missing, (
        f"REGRESSION: Post API contract broken — missing fields: {missing}"
    )
    logger.info("REG-011 PASSED — post API contract is intact.")


# ======================================================================
#  REG-012 — Negative regression: non-existent user still 404
# ======================================================================

@pytest.mark.regression
@pytest.mark.negative
def test_nonexistent_user_still_404(api_client: APIClient) -> None:
    """A non-existent user ID must still return 404 after any change."""
    response = api_client.get("/users/999999")

    assert response.status_code == 404, (
        f"REGRESSION: /users/999999 returned {response.status_code} — expected 404."
    )
    logger.info("REG-012 PASSED — non-existent user still returns 404.")


# ======================================================================
#  REG-013 — Negative regression: non-existent post still 404
# ======================================================================

@pytest.mark.regression
@pytest.mark.negative
def test_nonexistent_post_still_404(api_client: APIClient) -> None:
    """A non-existent post ID must still return 404 after any change."""
    response = api_client.get("/posts/999999")

    assert response.status_code == 404, (
        f"REGRESSION: /posts/999999 returned {response.status_code} — expected 404."
    )
    logger.info("REG-013 PASSED — non-existent post still returns 404.")


# ======================================================================
#  REG-014 — User-to-posts relationship
# ======================================================================

@pytest.mark.regression
def test_user_to_posts_relationship_intact(api_client: APIClient) -> None:
    """GET /users/1/posts must still return posts belonging to user 1."""
    response = api_client.get("/users/1/posts")
    assert response.status_code == 200

    posts = response.json()
    assert len(posts) > 0, "REGRESSION: User 1 has no posts — relationship broken."

    bad = [p["id"] for p in posts if p.get("userId") != 1]
    assert not bad, (
        f"REGRESSION: Posts with wrong userId returned: {bad}"
    )
    logger.info(
        "REG-014 PASSED — user-to-posts relationship intact (%d posts).", len(posts)
    )


# ======================================================================
#  REG-015 — Post-to-comments relationship
# ======================================================================

@pytest.mark.regression
def test_post_to_comments_relationship_intact(api_client: APIClient) -> None:
    """GET /posts/1/comments must still return comments for post 1."""
    response = api_client.get("/posts/1/comments")
    assert response.status_code == 200

    comments = response.json()
    assert len(comments) > 0, "REGRESSION: Post 1 has no comments — relationship broken."

    bad = [c["id"] for c in comments if c.get("postId") != 1]
    assert not bad, (
        f"REGRESSION: Comments with wrong postId returned: {bad}"
    )
    logger.info(
        "REG-015 PASSED — post-to-comments relationship intact (%d comments).",
        len(comments),
    )
