import uuid

import pytest

from api import projects as projects_api
from clients.auth import register_and_login
from clients.http_client import HttpClient
from config import get_base_url


@pytest.mark.regression
def test_create_project(client, project_factory):
    project_id = project_factory()

    resp = projects_api.get_project(client, project_id)
    client.expect_status(resp, 200)
    body = resp.json()
    assert body["id"] == project_id
    assert body["title"].startswith("qa-")


@pytest.mark.regression
def test_update_project(client, project_factory):
    project_id = project_factory()

    resp = projects_api.update_project(client, project_id, title="renamed-project")
    client.expect_status(resp, 200)
    assert resp.json()["title"] == "renamed-project"

    check = projects_api.get_project(client, project_id)
    assert check.json()["title"] == "renamed-project"


@pytest.mark.regression
def test_delete_project(client, project_factory):
    project_id = project_factory()

    resp = projects_api.delete_project(client, project_id)
    client.expect_status(resp, 200, 204)

    check = projects_api.get_project(client, project_id)
    client.expect_status(check, 404)


@pytest.mark.regression
def test_get_nonexistent_project(client):
    resp = projects_api.get_project(client, 999999999)
    client.expect_status(resp, 404)


@pytest.mark.regression
def test_create_project_with_empty_title(client):
    resp = projects_api.create_project(client, title="")
    client.expect_status(resp, 400,412, 422)


@pytest.mark.regression
def test_other_users_project_not_accessible(client, stand):

    resp = projects_api.create_project(client, title=f"qa-{uuid.uuid4().hex[:8]}")
    client.expect_status(resp, 200, 201)
    foreign_project_id = resp.json()["id"]

    try:
        base_url = get_base_url(stand)
        other = HttpClient(base_url=base_url)
        register_and_login(other)

        resp = projects_api.get_project(other, foreign_project_id)
        client.expect_status(resp, 403, 404)
    finally:
        projects_api.delete_project(client, foreign_project_id)


@pytest.mark.regression
def test_projects_pagination(client, project_factory):
    for _ in range(3):
        project_factory()

    all_resp = projects_api.list_projects(client)
    client.expect_status(all_resp, 200)
    all_count = len(all_resp.json())

    pag_resp = projects_api.list_projects(client, per_page=2)
    client.expect_status(pag_resp, 200)
    pag_count = len(pag_resp.json())

    assert pag_count < all_count, (
        f"Пагинация не работает: без per_page {all_count}, с per_page=2 {pag_count}"
    )

    headers_lower = {k.lower(): v for k, v in pag_resp.headers.items()}
    assert "x-pagination-total-pages" in headers_lower
    assert "x-pagination-result-count" in headers_lower