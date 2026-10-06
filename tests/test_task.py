import uuid

import pytest

from api import projects as projects_api
from api import tasks as tasks_api


@pytest.mark.regression
def test_create_task(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    resp = tasks_api.get_task(client, task_id)
    client.expect_status(resp, 200)
    body = resp.json()
    assert body["id"] == task_id
    assert body["title"].startswith("qa-")
    assert body["project_id"] == project_id


@pytest.mark.regression
def test_update_task(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    resp = tasks_api.update_task(client, task_id, title="renamed-task")
    client.expect_status(resp, 200)

    check = tasks_api.get_task(client, task_id)
    assert check.json()["title"] == "renamed-task"


@pytest.mark.regression
def test_delete_task(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    resp = tasks_api.delete_task(client, task_id)
    client.expect_status(resp, 200, 204)

    check = tasks_api.get_task(client, task_id)
    client.expect_status(check, 404)


@pytest.mark.regression
def test_get_nonexistent_task(client):
    resp = tasks_api.get_task(client, 999999999)
    client.expect_status(resp, 404)


@pytest.mark.regression
def test_create_task_with_empty_title(client, project_factory):
    project_id = project_factory()
    resp = tasks_api.create_task(client, project_id=project_id, title="")
    client.expect_status(resp, 400, 422)


@pytest.mark.regression
def test_list_tasks_in_project(client, project_factory, task_factory):
    project_id = project_factory()
    task_id_1 = task_factory(project_id)
    task_id_2 = task_factory(project_id)

    resp = tasks_api.list_tasks(client, project_id)
    client.expect_status(resp, 200)
    ids = {t["id"] for t in resp.json()}
    assert task_id_1 in ids
    assert task_id_2 in ids