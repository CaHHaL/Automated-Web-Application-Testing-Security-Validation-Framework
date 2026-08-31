"""
tests/api/test_validation.py
-----------------------------
Schema-level validation tests — verifying the structure, data types,
and values of API responses for all major endpoints.

Test IDs
--------
VAL-001  Users list — every item has all required fields
VAL-002  Posts list — every item has all required fields
VAL-003  Comments list — every item has all required fields
VAL-004  Todos list — every item has all required fields
VAL-005  User email format validation
VAL-006  Todo 'completed' field is a boolean
VAL-007  Post userId references a real user
VAL-008  Boundary IDs — min/max valid user IDs
VAL-009  Content-Type header is application/json
VAL-010  Parameterized field validation across post IDs
"""

import re

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

REQUIRED_USER_FIELDS = ["id", "name", "username", "email", "address", "phone", "website", "company"]
REQUIRED_POST_FIELDS = ["id", "userId", "title", "body"]
REQUIRED_COMMENT_FIELDS = ["id", "postId", "name", "email", "body"]
REQUIRED_TODO_FIELDS = ["id", "userId", "title", "completed"]


# ======================================================================
#  VAL-001 — Users list field validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_all_users_have_required_fields(api_client: APIClient) -> None:
    """Every user in /users must contain all required fields."""
    response = api_client.get("/users")
    assert response.status_code == 200

    users = response.json()
    for user in users:
        missing = [f for f in REQUIRED_USER_FIELDS if f not in user]
        assert not missing, (
            f"User id={user.get('id')} missing fields: {missing}"
        )

    logger.info(
        "VAL-001 PASSED — all %d users have required fields.", len(users)
    )


# ======================================================================
#  VAL-002 — Posts list field validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_all_posts_have_required_fields(api_client: APIClient) -> None:
    """Every post in /posts must contain all required fields."""
    response = api_client.get("/posts")
    assert response.status_code == 200

    posts = response.json()
    for post in posts:
        missing = [f for f in REQUIRED_POST_FIELDS if f not in post]
        assert not missing, (
            f"Post id={post.get('id')} missing fields: {missing}"
        )

    logger.info(
        "VAL-002 PASSED — all %d posts have required fields.", len(posts)
    )


# ======================================================================
#  VAL-003 — Comments list field validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_all_comments_have_required_fields(api_client: APIClient) -> None:
    """Every comment in /comments must contain all required fields."""
    response = api_client.get("/comments")
    assert response.status_code == 200

    comments = response.json()
    for comment in comments:
        missing = [f for f in REQUIRED_COMMENT_FIELDS if f not in comment]
        assert not missing, (
            f"Comment id={comment.get('id')} missing fields: {missing}"
        )

    logger.info(
        "VAL-003 PASSED — all %d comments have required fields.", len(comments)
    )


# ======================================================================
#  VAL-004 — Todos list field validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_all_todos_have_required_fields(api_client: APIClient) -> None:
    """Every todo in /todos must contain all required fields."""
    response = api_client.get("/todos")
    assert response.status_code == 200

    todos = response.json()
    for todo in todos:
        missing = [f for f in REQUIRED_TODO_FIELDS if f not in todo]
        assert not missing, (
            f"Todo id={todo.get('id')} missing fields: {missing}"
        )

    logger.info(
        "VAL-004 PASSED — all %d todos have required fields.", len(todos)
    )


# ======================================================================
#  VAL-005 — Email format validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_user_email_format(api_client: APIClient) -> None:
    """Every user email should match a basic email pattern."""
    response = api_client.get("/users")
    assert response.status_code == 200

    users = response.json()
    invalid_emails = [
        (u["id"], u["email"])
        for u in users
        if not EMAIL_REGEX.match(u.get("email", ""))
    ]
    assert not invalid_emails, f"Invalid email formats: {invalid_emails}"

    logger.info("VAL-005 PASSED — all user emails are valid.")


# ======================================================================
#  VAL-006 — Todo 'completed' is boolean
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_todo_completed_is_boolean(api_client: APIClient) -> None:
    """The 'completed' field on every todo must be a boolean."""
    response = api_client.get("/todos")
    assert response.status_code == 200

    todos = response.json()
    non_bool = [
        t["id"]
        for t in todos
        if not isinstance(t.get("completed"), bool)
    ]
    assert not non_bool, f"Todos with non-boolean 'completed': {non_bool}"

    logger.info("VAL-006 PASSED — all todo 'completed' fields are boolean.")


# ======================================================================
#  VAL-007 — Post userId references a real user
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_post_user_id_references_valid_user(api_client: APIClient) -> None:
    """The userId of the first post should correspond to an existing user."""
    post_resp = api_client.get("/posts/1")
    assert post_resp.status_code == 200

    user_id = post_resp.json().get("userId")
    user_resp = api_client.get(f"/users/{user_id}")

    assert user_resp.status_code == 200, (
        f"userId={user_id} from post does not resolve to a valid user."
    )
    logger.info(
        "VAL-007 PASSED — post userId=%d resolves to a valid user.", user_id
    )


# ======================================================================
#  VAL-008 — Boundary IDs
# ======================================================================

@pytest.mark.api
@pytest.mark.boundary
@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (1,  200),   # minimum valid
        (10, 200),   # maximum valid (JSONPlaceholder has 10 users)
        (0,  404),   # below minimum
        (11, 404),   # above maximum
    ],
)
def test_user_id_boundaries(
    api_client: APIClient, user_id: int, expected_status: int
) -> None:
    """Boundary user IDs should return the expected HTTP status."""
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == expected_status, (
        f"user_id={user_id}: expected {expected_status}, "
        f"got {response.status_code}"
    )
    logger.info(
        "VAL-008 PASSED — /users/%d returned %d.", user_id, response.status_code
    )


# ======================================================================
#  VAL-009 — Content-Type header
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_response_content_type_is_json(api_client: APIClient) -> None:
    """API responses should declare Content-Type: application/json."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Expected JSON content-type, got: {content_type}"
    )
    logger.info("VAL-009 PASSED — Content-Type is application/json.")


# ======================================================================
#  VAL-010 — Parameterized post field validation
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
@pytest.mark.parametrize("post_id", [1, 10, 50, 100])
def test_post_fields_parameterized(api_client: APIClient, post_id: int) -> None:
    """Each sampled post ID should return a complete post object."""
    response = api_client.get(f"/posts/{post_id}")
    assert response.status_code == 200, (
        f"Expected 200 for post_id={post_id}, got {response.status_code}"
    )

    post = response.json()
    missing = [f for f in REQUIRED_POST_FIELDS if f not in post]
    assert not missing, (
        f"Post id={post_id} missing fields: {missing}"
    )
    logger.info(
        "VAL-010 PASSED — post_id=%d has all required fields.", post_id
    )
