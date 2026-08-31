"""
tests/functional/test_functional.py
-------------------------------------
Functional tests — end-to-end CRUD workflow validation.

These tests verify that the application behaves according to its
expected functional requirements across complete workflows, not just
individual endpoints.

Test IDs
--------
FUNC-001  Create a new post — HTTP 201, fields echoed back
FUNC-002  Read the created post — HTTP 200, correct data
FUNC-003  Update a post (PUT) — HTTP 200, title updated
FUNC-004  Partially update a post (PATCH) — HTTP 200, field updated
FUNC-005  Delete a post — HTTP 200, resource removed
FUNC-006  Create a comment — HTTP 201
FUNC-007  Create a todo — HTTP 201
FUNC-008  List all todos for a user — HTTP 200, non-empty
FUNC-009  Filter posts by userId — all returned posts belong to the user
FUNC-010  Filter comments by postId — all comments belong to the post
"""

import pytest

from utils.api_client import APIClient
from utils.logger import get_logger

logger = get_logger(__name__)

NEW_POST = {
    "title": "WebTestX — Functional Test Post",
    "body": "Created automatically by the WebTestX functional test suite.",
    "userId": 1,
}


# ======================================================================
#  FUNC-001 — Create a new post (POST /posts)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_create_post(api_client: APIClient) -> None:
    """POST /posts should return HTTP 201 with the created resource."""
    response = api_client.post("/posts", json=NEW_POST)

    assert response.status_code == 201, (
        f"Expected 201, got {response.status_code}"
    )
    data = response.json()
    assert "id" in data, "Created post should have an 'id' field."
    assert data["title"] == NEW_POST["title"]
    assert data["body"] == NEW_POST["body"]
    assert data["userId"] == NEW_POST["userId"]

    logger.info("FUNC-001 PASSED — created post id=%s.", data.get("id"))


# ======================================================================
#  FUNC-002 — Read an existing post (GET /posts/1)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_read_post(api_client: APIClient) -> None:
    """GET /posts/1 should return HTTP 200 with the expected post."""
    response = api_client.get("/posts/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data and len(data["title"]) > 0
    assert "body" in data and len(data["body"]) > 0

    logger.info("FUNC-002 PASSED — read post id=1.")


# ======================================================================
#  FUNC-003 — Full update of a post (PUT /posts/1)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_update_post_full(api_client: APIClient) -> None:
    """PUT /posts/1 should return HTTP 200 with the updated title."""
    updated = {
        "id": 1,
        "title": "WebTestX Updated Title",
        "body": "Full update by WebTestX PUT test.",
        "userId": 1,
    }
    response = api_client.put("/posts/1", json=updated)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}"
    )
    data = response.json()
    assert data["title"] == updated["title"]

    logger.info("FUNC-003 PASSED — full update of post id=1.")


# ======================================================================
#  FUNC-004 — Partial update of a post (PATCH /posts/1)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_update_post_partial(api_client: APIClient) -> None:
    """PATCH /posts/1 should return HTTP 200 with the patched field."""
    patch_data = {"title": "WebTestX Patched Title"}
    response = api_client.patch("/posts/1", json=patch_data)

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}"
    )
    data = response.json()
    assert data["title"] == patch_data["title"]

    logger.info("FUNC-004 PASSED — partial update of post id=1.")


# ======================================================================
#  FUNC-005 — Delete a post (DELETE /posts/1)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_delete_post(api_client: APIClient) -> None:
    """DELETE /posts/1 should return HTTP 200 (JSONPlaceholder simulates deletion)."""
    response = api_client.delete("/posts/1")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}"
    )
    logger.info("FUNC-005 PASSED — delete post id=1.")


# ======================================================================
#  FUNC-006 — Create a comment (POST /comments)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_create_comment(api_client: APIClient) -> None:
    """POST /comments should return HTTP 201 with the new comment."""
    new_comment = {
        "postId": 1,
        "name": "WebTestX Automated Comment",
        "email": "webtestx@example.com",
        "body": "This comment was created by the WebTestX test suite.",
    }
    response = api_client.post("/comments", json=new_comment)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == new_comment["email"]

    logger.info("FUNC-006 PASSED — created comment id=%s.", data.get("id"))


# ======================================================================
#  FUNC-007 — Create a todo (POST /todos)
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_create_todo(api_client: APIClient) -> None:
    """POST /todos should return HTTP 201 with the new todo."""
    new_todo = {
        "userId": 1,
        "title": "WebTestX Automated Todo",
        "completed": False,
    }
    response = api_client.post("/todos", json=new_todo)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == new_todo["title"]
    assert data["completed"] is False

    logger.info("FUNC-007 PASSED — created todo id=%s.", data.get("id"))


# ======================================================================
#  FUNC-008 — List todos for a specific user
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_list_user_todos(api_client: APIClient) -> None:
    """GET /users/1/todos should return HTTP 200 with a non-empty list."""
    response = api_client.get("/users/1/todos")

    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list) and len(todos) > 0

    for todo in todos:
        assert todo["userId"] == 1, (
            f"Todo userId {todo.get('userId')} != 1"
        )

    logger.info(
        "FUNC-008 PASSED — %d todos for user 1.", len(todos)
    )


# ======================================================================
#  FUNC-009 — Filter posts by userId
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_filter_posts_by_user(api_client: APIClient) -> None:
    """GET /posts?userId=1 should return only posts belonging to user 1."""
    response = api_client.get("/posts", params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0, "User 1 should have at least one post."

    for post in posts:
        assert post["userId"] == 1, (
            f"Post userId {post.get('userId')} != 1"
        )

    logger.info(
        "FUNC-009 PASSED — %d posts for userId=1.", len(posts)
    )


# ======================================================================
#  FUNC-010 — Filter comments by postId
# ======================================================================

@pytest.mark.functional
@pytest.mark.positive
def test_filter_comments_by_post(api_client: APIClient) -> None:
    """GET /comments?postId=1 should return only comments for post 1."""
    response = api_client.get("/comments", params={"postId": 1})

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0, "Post 1 should have at least one comment."

    for comment in comments:
        assert comment["postId"] == 1, (
            f"Comment postId {comment.get('postId')} != 1"
        )

    logger.info(
        "FUNC-010 PASSED — %d comments for postId=1.", len(comments)
    )
