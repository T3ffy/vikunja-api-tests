import os
import pytest
import requests


BASE_URL = "http://localhost:3456"
TEST_USER = os.getenv("TEST_USER", "qa-owner")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "TestPass123!")


@pytest.fixture(scope="module")
def contract_token() -> str:
    resp = requests.post(
        f"{BASE_URL}/api/v1/login",
        json={"username": TEST_USER, "password": TEST_PASSWORD},
        timeout=10,
    )
    if resp.status_code == 429:
        pytest.skip("Rate limit при логине")
    resp.raise_for_status()
    return resp.json()["token"]


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="VK-001: PUT /user/settings/webhooks/events returns 400 instead of 405",
)
def test_put_returns_405_not_400(contract_token):
    resp = requests.put(
        f"{BASE_URL}/api/v2/user/settings/webhooks/events",
        headers={"Authorization": f"Bearer {contract_token}"},
        timeout=10,
    )
    assert resp.status_code == 405, (
        f"VK-001: Ожидается 405 Method Not Allowed, получено {resp.status_code}. "
        f"Тело: {resp.text[:200]}"
    )


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="VK-002: PUT /projects/{id}/views/{id}/buckets/tasks returns 400 instead of 405",
)
def test_put_bucket_tasks_returns_405_not_400(contract_token):
    resp = requests.put(
        f"{BASE_URL}/api/v2/projects/1/views/1/buckets/tasks",
        headers={"Authorization": f"Bearer {contract_token}"},
        timeout=10,
    )
    assert resp.status_code == 405, (
        f"VK-002: Ожидается 405 Method Not Allowed, получено {resp.status_code}. "
        f"Тело: {resp.text[:200]}"
    )


@pytest.mark.contract
@pytest.mark.xfail(
    strict=True,
    reason="VK-003: /avatar/{username} returns image/svg+xml instead of application/octet-stream",
)
def test_avatar_content_type(contract_token):
    resp = requests.get(
        f"{BASE_URL}/api/v2/avatar/{TEST_USER}",
        headers={"Authorization": f"Bearer {contract_token}"},
        timeout=10,
    )
    assert resp.status_code == 200
    content_type = resp.headers.get("Content-Type", "")
    assert "application/octet-stream" in content_type, (
        f"VK-003: Ожидается application/octet-stream, получено {content_type}"
    )