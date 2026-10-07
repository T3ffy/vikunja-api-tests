import pytest

from api import teams as teams_api
from api import shares as shares_api
from api import projects as projects_api


@pytest.mark.regression
@pytest.mark.mutating
def test_create_team(client, team_factory):
    team_id = team_factory()
    assert isinstance(team_id, int)


@pytest.mark.regression
@pytest.mark.mutating
def test_share_project_with_team_write(client, second_user, project_factory, team_factory):
    project_id = project_factory()
    team_id = team_factory()

    me_resp = second_user.get("/user")
    second_username = me_resp.json()["username"]
    teams_api.add_member(client, team_id, second_username)

    resp = teams_api.share_project_with_team(client, project_id, team_id, right=1)
    client.expect_status(resp, 200, 201)

    create_resp = second_user.put(f"/projects/{project_id}/tasks", json={"title": "qa-team-task"})
    second_user.expect_status(create_resp, 200, 201)


@pytest.mark.regression
@pytest.mark.parametrize("team_right,expected", [
    (0, False),  
    (1, True),   
    (2, True),   
])
def test_team_permission_matrix(client, second_user, project_factory, team_factory, team_right, expected):
    project_id = project_factory()
    team_id = team_factory()

    me_resp = second_user.get("/user")
    teams_api.add_member(client, team_id, me_resp.json()["username"])
    teams_api.share_project_with_team(client, project_id, team_id, right=team_right)

    create_resp = second_user.put(f"/projects/{project_id}/tasks", json={"title": "qa-team-task"})
    if expected:
        second_user.expect_status(create_resp, 200, 201)
    else:
        second_user.expect_status(create_resp, 403, 404)