from clients.http_client import HttpClient


def share_project_with_user(client: HttpClient, project_id: int, username: str, right: int) -> "requests.Response":
    return client.put(f"/projects/{project_id}/users", json={"username": username, "permission": right})


def remove_user_share(client: HttpClient, project_id: int, username: str) -> "requests.Response":
    return client.delete(f"/projects/{project_id}/users/{username}")