import uuid
import pytest

from api import projects as projects_api
from api import tasks as tasks_api
from config import get_base_url
from clients.http_client import HttpClient
from clients.auth import register_and_login


def pytest_addoption(parser):
    parser.addoption(
        "--stand",
        action="store",
        default="local",
    )


@pytest.fixture(scope="session")
def stand(request) -> str:
    return request.config.getoption("--stand")


@pytest.fixture
def client(stand: str) -> HttpClient:
    base_url = get_base_url(stand)
    http = HttpClient(base_url=base_url)
    register_and_login(http)
    return http

@pytest.fixture(scope="session")
def stand(request) -> str:
    return request.config.getoption("--stand")

@pytest.fixture (scope="session")
def client(stand:str) -> HttpClient:
    base_url=get_base_url(stand)
    http= HttpClient(base_url=base_url)
    register_and_login(http)
    return http

@pytest.fixture
def project_factory(client):
    created_ids = []

    def _create(title: str | None = None, **extra) -> int:
        unique_title = title or f"qa-{uuid.uuid4().hex[:8]}"
        resp = projects_api.create_project(client, title=unique_title, **extra)
        client.expect_status(resp, 200, 201)
        project_id = resp.json()["id"]
        created_ids.append(project_id)
        return project_id

    yield _create
    for project_id in created_ids:
        projects_api.delete_project(client, project_id)


@pytest.fixture
def task_factory(client):
    created_ids = []

    def _create(project_id: int, title: str | None = None, **extra) -> int:
        unique_title = title or f"qa-{uuid.uuid4().hex[:8]}"
        resp = tasks_api.create_task(client, project_id=project_id, title=unique_title, **extra)
        client.expect_status(resp, 200, 201)
        task_id = resp.json()["id"]
        created_ids.append(task_id)
        return task_id

    yield _create

    for task_id in created_ids:
        tasks_api.delete_task(client, task_id)