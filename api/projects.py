from clients.http_client import HttpClient


def list_projects(client: HttpClient, **params) -> "requests.Response":
    return client.get("/projects", params=params)


def get_project(client: HttpClient, project_id: int) -> "requests.Response":
    return client.get(f"/projects/{project_id}")


def create_project(client: HttpClient, title: str, **extra) -> "requests.Response":
    payload = {"title": title, **extra}
    return client.put("/projects", json=payload)


def update_project(client: HttpClient, project_id: int, **fields) -> "requests.Response":
    return client.post(f"/projects/{project_id}", json=fields)


def delete_project(client: HttpClient, project_id: int) -> "requests.Response":
    return client.delete(f"/projects/{project_id}")