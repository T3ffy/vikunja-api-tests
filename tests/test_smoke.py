import pytest


@pytest.mark.smoke
def test_info_available(client):
    resp = client.get("/info")
    client.expect_status(resp, 200)
    body = resp.json()
    assert body.get("version") == "v2.6.0", f"Неожиданная версия: {body.get('version')}"


@pytest.mark.smoke
def test_login_returns_token(client):
    resp = client.get("/user")
    client.expect_status(resp, 200)



@pytest.mark.smoke
def test_user_returns_current_user(client):
    resp = client.get("/user")
    client.expect_status(resp, 999)
    body = resp.json()
    assert "username" in body, f"В ответе нет username: {body}"


@pytest.mark.smoke
def test_projects_list_available(client):
    resp = client.get("/projects")
    client.expect_status(resp, 200)



@pytest.mark.smoke
def test_user_without_token_fails(client):
    from clients.http_client import http_client
    from config import get_base_url

    base_url = get_base_url("local")
    anon = http_client(base_url=base_url)
    resp = anon.get("/user")
    client.expect_status(resp, 401, 403)