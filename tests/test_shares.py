import pytest
from api import projects as projects_api
from api import shares as shares_api


NONEXISTENT_USER = "qa-nonexistent-user-xyz-9999"
PERMISSION_MATRIX = [

    (0, True, False, False, False, False),   
    (1, True, True, True, False, False),     
    (2, True, True, True, True, True),      
]


@pytest.mark.regression
@pytest.mark.mutating
@pytest.mark.parametrize("right,can_read,can_create_task,can_update_project,can_delete_project,can_share", PERMISSION_MATRIX)
def test_user_permission_matrix(
    client, second_user, project_factory, task_factory,
    right, can_read, can_create_task, can_update_project, can_delete_project, can_share,
):
    project_id = project_factory()

    me_resp = second_user.get("/user")
    second_username = me_resp.json()["username"]
    resp = shares_api.share_project_with_user(client, project_id, second_username, right)
    client.expect_status(resp, 200, 201)

    get_resp = second_user.get(f"/projects/{project_id}")
    if can_read:
        second_user.expect_status(get_resp, 200)
    else:
        second_user.expect_status(get_resp, 403, 404)

    create_task_resp = second_user.put(f"/projects/{project_id}/tasks", json={"title": f"qa-{right}"})
    if can_create_task:
        second_user.expect_status(create_task_resp, 200, 201)
    else:
        second_user.expect_status(create_task_resp, 403, 404)

    update_resp = second_user.post(f"/projects/{project_id}", json={"title": "renamed"})
    if can_update_project:
        second_user.expect_status(update_resp, 200)
    else:
        second_user.expect_status(update_resp, 403, 404)

    delete_resp = second_user.delete(f"/projects/{project_id}")
    if can_delete_project:
        second_user.expect_status(delete_resp, 200, 204)
    else:
        second_user.expect_status(delete_resp, 403, 404)


@pytest.mark.regression
@pytest.mark.mutating
def test_owner_can_delete_project(client, project_factory):
    project_id = project_factory()
    resp = projects_api.delete_project(client, project_id)
    client.expect_status(resp, 200, 204)


@pytest.mark.regression
def test_stranger_cannot_read_project(client, second_user, project_factory):
    project_id = project_factory()
    resp = second_user.get(f"/projects/{project_id}")
    second_user.expect_status(resp, 403, 404)


@pytest.mark.regression
@pytest.mark.parametrize("right,expected_allowed", [
    (0, False), 
    (1, False),  
    (2, True),  
])
def test_user_can_share_project(client, second_user, project_factory, right, expected_allowed):
    project_id = project_factory()
    me_resp = second_user.get("/user")
    second_username = me_resp.json()["username"]


    shares_api.share_project_with_user(client, project_id, second_username, right)
    resp = shares_api.share_project_with_user(second_user, project_id, NONEXISTENT_USER, right=0)
    if expected_allowed:
        second_user.expect_status(resp, 200, 201, 404) 
    else:
        second_user.expect_status(resp, 403)