"""
tests/api/test_users.py
-----------------------
Positive API tests for the /users endpoint.

Test IDs
--------
API-001  Retrieve all users — HTTP 200, non-empty list
API-002  Retrieve a single valid user — HTTP 200, correct ID
API-003  Validate required fields on a user object
API-004  Verify user response time is within acceptable limits
API-005  Parameterized — retrieve multiple known-valid user IDs
API-006  Validate nested address fields on a user object
API-007  Validate nested company fields on a user object
API-008  Retrieve user posts — HTTP 200, non-empty list
"""

import time

import pytest

from utils.api_client import APIClient
from utils.config import config
from utils.logger import get_logger

logger = get_logger(__name__)

REQUIRED_USER_FIELDS = [
    "id", "name", "username", "email",
    "address", "phone", "website", "company",
]
REQUIRED_ADDRESS_FIELDS = ["street", "suite", "city", "zipcode", "geo"]
REQUIRED_COMPANY_FIELDS = ["name", "catchPhrase", "bs"]


# ======================================================================
#  API-001 — Retrieve all users
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_get_all_users(api_client: APIClient) -> None:
    """GET /users should return HTTP 200 and a non-empty list."""
    response = api_client.get("/users")

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}"
    )

    data = response.json()
    assert isinstance(data, list), "Response body should be a JSON array."
    assert len(data) > 0, "User list should not be empty."

    logger.info("test_get_all_users PASSED — %d users returned.", len(data))


# ======================================================================
#  API-002 — Retrieve a single valid user
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_get_single_user(api_client: APIClient) -> None:
    """GET /users/1 should return HTTP 200 with id == 1."""
    response = api_client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1, f"Expected id=1, got id={data.get('id')}"

    logger.info("test_get_single_user PASSED — user id=%s", data["id"])


# ======================================================================
#  API-003 — Validate required fields
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_user_required_fields(api_client: APIClient) -> None:
    """Every required field should be present in the user object."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    data = response.json()
    missing = [f for f in REQUIRED_USER_FIELDS if f not in data]
    assert not missing, f"Missing required fields: {missing}"

    logger.info("test_user_required_fields PASSED — all fields present.")


# ======================================================================
#  API-004 — Response time
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_user_response_time(api_client: APIClient) -> None:
    """API response should arrive within the configured time limit."""
    start = time.perf_counter()
    response = api_client.get("/users/1")
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert response.status_code == 200
    assert elapsed_ms < config.MAX_RESPONSE_TIME_MS, (
        f"Response took {elapsed_ms:.0f} ms — limit is {config.MAX_RESPONSE_TIME_MS} ms."
    )

    logger.info(
        "test_user_response_time PASSED — response in %.0f ms.", elapsed_ms
    )


# ======================================================================
#  API-005 — Parameterized retrieval of multiple users
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
@pytest.mark.parametrize("user_id", [1, 2, 3, 5, 7, 10])
def test_get_valid_user_parameterized(api_client: APIClient, user_id: int) -> None:
    """GET /users/{id} returns HTTP 200 for each known-valid user ID."""
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == 200, (
        f"Expected 200 for user_id={user_id}, got {response.status_code}"
    )
    data = response.json()
    assert data["id"] == user_id, (
        f"Response id {data.get('id')} does not match requested id {user_id}"
    )

    logger.info(
        "test_get_valid_user_parameterized PASSED — user_id=%d", user_id
    )


# ======================================================================
#  API-006 — Nested address fields
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_user_address_fields(api_client: APIClient) -> None:
    """The 'address' object should contain all required nested fields."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    address = response.json().get("address", {})
    missing = [f for f in REQUIRED_ADDRESS_FIELDS if f not in address]
    assert not missing, f"Missing address fields: {missing}"

    geo = address.get("geo", {})
    assert "lat" in geo, "'geo' should contain 'lat'."
    assert "lng" in geo, "'geo' should contain 'lng'."

    logger.info("test_user_address_fields PASSED.")


# ======================================================================
#  API-007 — Nested company fields
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_user_company_fields(api_client: APIClient) -> None:
    """The 'company' object should contain all required nested fields."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    company = response.json().get("company", {})
    missing = [f for f in REQUIRED_COMPANY_FIELDS if f not in company]
    assert not missing, f"Missing company fields: {missing}"

    logger.info("test_user_company_fields PASSED.")


# ======================================================================
#  API-008 — Retrieve posts by user
# ======================================================================

@pytest.mark.api
@pytest.mark.positive
def test_get_user_posts(api_client: APIClient) -> None:
    """GET /users/1/posts should return HTTP 200 with a non-empty list."""
    response = api_client.get("/users/1/posts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) and len(data) > 0, (
        "User 1 should have at least one post."
    )

    for post in data:
        assert post["userId"] == 1, (
            f"Post userId {post.get('userId')} != 1"
        )

    logger.info(
        "test_get_user_posts PASSED — %d posts returned.", len(data)
    )