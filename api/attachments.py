from clients.http_client import HttpClient


def upload_attachment(client: HttpClient, task_id: int, filename: str, content: bytes) -> "requests.Response":
    files = {"files": (filename, content)}
    return client.put(f"/tasks/{task_id}/attachments", files=files)


def list_attachments(client: HttpClient, task_id: int) -> "requests.Response":
    return client.get(f"/tasks/{task_id}/attachments")


def download_attachment(client: HttpClient, task_id: int, attachment_id: int) -> "requests.Response":
    return client.get(f"/tasks/{task_id}/attachments/{attachment_id}")


def delete_attachment(client: HttpClient, task_id: int, attachment_id: int) -> "requests.Response":
    return client.delete(f"/tasks/{task_id}/attachments/{attachment_id}")