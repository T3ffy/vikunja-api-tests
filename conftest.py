import uuid
import pytest


from api import projects as projects_api
from api import tasks as tasks_api
from api import shares as shares_api
from api import teams as teams_api
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


@pytest.fixture(scope="session")
def client(stand: str) -> HttpClient:
    base_url = get_base_url(stand)
    http = HttpClient(base_url=base_url)
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

@pytest.fixture(scope="session")
def second_user(stand: str) -> HttpClient:
    base_url = get_base_url(stand)
    http = HttpClient(base_url=base_url)
    register_and_login(http)
    return http


@pytest.fixture
def user_factory(stand: str):
    created = []

    def _create() -> HttpClient:
        base_url = get_base_url(stand)
        http = HttpClient(base_url=base_url)
        register_and_login(http)
        created.append(http)
        return http

    yield _create


@pytest.fixture
def team_factory(client):
    created_ids = []

    def _create(name: str | None = None) -> int:
        unique_name = name or f"qa-team-{uuid.uuid4().hex[:8]}"
        resp = teams_api.create_team(client, unique_name)
        client.expect_status(resp, 200, 201)
        team_id = resp.json()["id"]
        created_ids.append(team_id)
        return team_id

    yield _create

    for team_id in created_ids:
        teams_api.delete_team(client, team_id)


@pytest.fixture
def project_with_share(client, second_user, project_factory):
    project_id = project_factory()
    me_resp = second_user.get("/user")
    second_user.get("/user")
    second_username = me_resp.json()["username"]
    resp = shares_api.share_project_with_user(client, project_id, second_username, right=1)
    client.expect_status(resp, 200, 201)
    return project_id, second_user
