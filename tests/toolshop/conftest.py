import pytest
import requests

from config import load_env


@pytest.fixture(scope="session")
def toolshop_base_url(stand: str) -> str:
    env = load_env(stand)
    return env["BASE_URL"]


@pytest.fixture(scope="session")
def admin_token(toolshop_base_url: str) -> str:
    resp = requests.post(
        f"{toolshop_base_url}/users/login",
        json={
            "email": "admin@practicesoftwaretesting.com",
            "password": "welcome01",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def customer_token(toolshop_base_url: str) -> str:
    resp = requests.post(
        f"{toolshop_base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def customer2_token(toolshop_base_url: str) -> str:
    resp = requests.post(
        f"{toolshop_base_url}/users/login",
        json={
            "email": "customer2@practicesoftwaretesting.com",
            "password": "welcome01",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


@pytest.fixture(scope="session")
def customer_user_id(toolshop_base_url: str, customer_token: str) -> int:
    resp = requests.get(
        f"{toolshop_base_url}/users/me",
        headers={"Authorization": f"Bearer {customer_token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["id"]