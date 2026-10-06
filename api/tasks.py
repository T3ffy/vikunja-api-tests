"""Функции для работы с эндпоинтами /tasks Vikunja."""

from clients.http_client import HttpClient


def list_tasks(client: HttpClient, project_id: int, **params) -> "requests.Response":
    return client.get(f"/projects/{project_id}/tasks", params=params)


def get_task(client: HttpClient, task_id: int) -> "requests.Response":
    return client.get(f"/tasks/{task_id}")


def create_task(client: HttpClient, project_id: int, title: str, **extra) -> "requests.Response":
    payload = {"title": title, **extra}
    return client.put(f"/projects/{project_id}/tasks", json=payload)


def update_task(client: HttpClient, task_id: int, **fields) -> "requests.Response":
    return client.post(f"/tasks/{task_id}", json=fields)


def delete_task(client: HttpClient, task_id: int) -> "requests.Response":
    return client.delete(f"/tasks/{task_id}")