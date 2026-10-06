import uuid
import requests

from clients.http_client import HttpClient


def register_and_login(client: HttpClient) -> str:
    username = f"qa_{uuid.uuid4().hex[:8]}"
    password = "TestPass123!"


    register_payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password": password,
    }
    resp = client.post("/register", json=register_payload)
    client.expect_status(resp, 201, 200)


    login_payload = {"username": username, "password": password}
    resp = client.post("/login", json=login_payload)
    client.expect_status(resp, 200)

    token = resp.json().get("token")
    if not token:
        raise AssertionError(f"В ответе логина нет токена: {resp.text[:200]}")

    client.set_token(token)
    return token