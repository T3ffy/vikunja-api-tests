import os
import pytest
import schemathesis
import requests


BASE_URL = "http://localhost:3456"
TEST_USER = os.getenv("TEST_USER", "qa-owner")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "TestPass123!")


def _get_token() -> str:
    resp = requests.post(
        f"{BASE_URL}/api/v1/login",
        json={"username": TEST_USER, "password": TEST_PASSWORD},
        timeout=10,
    )
    if resp.status_code == 429:
        pytest.skip("Rate limit при логине")
    resp.raise_for_status()
    return resp.json()["token"]


TOKEN = _get_token()
assert TOKEN, "Токен не получен"


schema = schemathesis.openapi.from_url(f"{BASE_URL}/api/v2/openapi.json")
schema = schema.include(method="GET")


@schema.parametrize()
def test_get_endpoints_conform_to_spec(case):
    case.headers = case.headers or {}
    case.headers["Authorization"] = f"Bearer {TOKEN}"

    response = case.call()

    if response.status_code == 429:
        pytest.skip("Rate limit")

    case.validate_response(response)