from clients.http_client import HttpClient


def create_team(client: HttpClient, name: str) -> "requests.Response":
    return client.put("/teams", json={"name": name})


def add_member(client: HttpClient, team_id: int, username: str, admin: bool = False) -> "requests.Response":
    return client.put(f"/teams/{team_id}/members", json={"username": username, "admin": admin})


def share_project_with_team(client: HttpClient, project_id: int, team_id: int, right: int) -> "requests.Response":
    return client.put(f"/projects/{project_id}/teams", json={"team_id": team_id, "permission": right})


def delete_team(client: HttpClient, team_id: int) -> "requests.Response":
    return client.delete(f"/teams/{team_id}")