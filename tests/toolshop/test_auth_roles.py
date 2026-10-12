import uuid

import pytest
import requests

@pytest.mark.toolshop
@pytest.mark.regression
@pytest.mark.xfail(
    strict=True,
    reason="TS-001: BOLA — customer can read other user's profile",
    condition="config.getoption('--stand') == 'pst-bugs'",
)
def test_user_cannot_read_other_profile(
    toolshop_base_url, customer_token, customer2_token
):
    me2 = requests.get(
        f"{toolshop_base_url}/users/me",
        headers={"Authorization": f"Bearer {customer2_token}"},
        timeout=10,
    )
    if me2.status_code == 404:
        pytest.skip("/users/me не поддерживается")
    me2.raise_for_status()
    other_id = me2.json()["id"]

    resp = requests.get(
        f"{toolshop_base_url}/users/{other_id}",
        headers={"Authorization": f"Bearer {customer_token}"},
        timeout=10,
    )
    assert resp.status_code in (403, 404), (
        f"Customer прочитал чужой профиль: {resp.status_code}. "
        f"Тело: {resp.text[:200]}"
    )


@pytest.mark.toolshop
@pytest.mark.regression
@pytest.mark.xfail(
    strict=True,
    reason="TS-002: Excessive Data Exposure — password и role в ответе",
    condition="config.getoption('--stand') == 'pst-bugs'",
)
def test_user_response_has_no_sensitive_fields(
    toolshop_base_url, customer_token, customer_user_id
):
    resp = requests.get(
        f"{toolshop_base_url}/users/{customer_user_id}",
        headers={"Authorization": f"Bearer {customer_token}"},
        timeout=10,
    )
    resp.raise_for_status()
    body = resp.json()

    forbidden = {"password", "password_hash", "role", "is_admin", "secret", "token"}
    found = forbidden & set(body.keys())

    assert not found, (
        f"В ответе /users/{customer_user_id} найдены служебные поля: {found}. "
        f"Все поля: {list(body.keys())}"
    )


@pytest.mark.toolshop
@pytest.mark.mutating
@pytest.mark.xfail(
    strict=True,
    reason="TS-003: BFLA — customer может удалить бренд",
    condition="config.getoption('--stand') == 'pst-bugs'",
)
def test_customer_cannot_delete_brand(
    toolshop_base_url, admin_token, customer_token
):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    customer_headers = {"Authorization": f"Bearer {customer_token}"}

    unique_name = f"qa-{uuid.uuid4().hex[:8]}"
    create_resp = requests.post(
        f"{toolshop_base_url}/brands",
        json={"name": unique_name, "slug": unique_name},
        headers=admin_headers,
        timeout=10,
)
    create_resp.raise_for_status()
    brand_id = create_resp.json()["id"]

    try:
        resp = requests.delete(
            f"{toolshop_base_url}/brands/{brand_id}",
            headers=customer_headers,
            timeout=10,
        )
        assert resp.status_code in (403, 404), (
            f"Customer удалил бренд: {resp.status_code}. "
            f"Тело: {resp.text[:200]}"
        )
    finally:
        requests.delete(
            f"{toolshop_base_url}/brands/{brand_id}",
            headers=admin_headers,
            timeout=10,
        )



@pytest.mark.toolshop
@pytest.mark.regression
def test_customer_sees_only_own_invoices(
    toolshop_base_url, customer_token, customer2_token
):
    customer_headers = {"Authorization": f"Bearer {customer_token}"}
    customer2_headers = {"Authorization": f"Bearer {customer2_token}"}

    resp1 = requests.get(
        f"{toolshop_base_url}/invoices",
        headers=customer_headers,
        timeout=10,
    )
    resp1.raise_for_status()
    customer_invoices = resp1.json()

    resp2 = requests.get(
        f"{toolshop_base_url}/invoices",
        headers=customer2_headers,
        timeout=10,
    )
    resp2.raise_for_status()
    customer2_invoices = resp2.json()

    if isinstance(customer_invoices, list) and isinstance(customer2_invoices, list):
        customer_ids = {inv["id"] for inv in customer_invoices if "id" in inv}
        customer2_ids = {inv["id"] for inv in customer2_invoices if "id" in inv}
        overlap = customer_ids & customer2_ids
        assert not overlap, (
            f"Customer видит счета customer2. Пересечение по id: {overlap}"
        )



@pytest.mark.toolshop
@pytest.mark.regression
@pytest.mark.mutating
@pytest.mark.xfail(
    strict=True,
    reason="TS-003: BFLA — customer может удалить бренд (204 вместо 403)",
    condition="config.getoption('--stand') == 'pst-bugs'",
)
def test_wrong_role_returns_403_not_401(
    toolshop_base_url, admin_token, customer_token
):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    customer_headers = {"Authorization": f"Bearer {customer_token}"}

    unique_name = f"qa-{uuid.uuid4().hex[:8]}"
    create_resp = requests.post(
        f"{toolshop_base_url}/brands",
        json={"name": unique_name, "slug": unique_name},
        headers=admin_headers,
        timeout=10,
    )
    create_resp.raise_for_status()
    brand_id = create_resp.json()["id"]

    try:
        resp = requests.delete(
            f"{toolshop_base_url}/brands/{brand_id}",
            headers=customer_headers,
            timeout=10,
        )
        assert resp.status_code == 403, (
            f"Ожидается 403, получено- {resp.status_code}. "
            f"Тело: {resp.text[:200]}"
        )
    finally:
        requests.delete(
            f"{toolshop_base_url}/brands/{brand_id}",
            headers=admin_headers,
            timeout=10,
        )