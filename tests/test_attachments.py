import pytest

from api import attachments as attachments_api
from api import shares as shares_api
from api import tasks as tasks_api



def _share_with(client, project_id, username, permission):
    resp = shares_api.share_project_with_user(client, project_id, username, permission)
    client.expect_status(resp, 200, 201)


def _username(client):
    return client.get("/user").json()["username"]


@pytest.mark.regression
@pytest.mark.mutating
def test_upload_and_download_same_bytes(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    content = b"hello, vikunja attachments!"

    upload = attachments_api.upload_attachment(client, task_id, "hello.txt", content)
    client.expect_status(upload, 200, 201)
    print("\n=== UPLOAD RESPONSE ===")
    print(f"Status: {upload.status_code}")
    print(f"Headers: {dict(upload.headers)}")
    print(f"Body: {upload.text[:500]}")
    print("=== END ===")
    attachment_id = upload.json()["success"][0]["id"]

    download = attachments_api.download_attachment(client, task_id, attachment_id)
    client.expect_status(download, 200)
    assert download.content == content, (
        f"Содержимое не совпадает.\n"
        f"  Загружено: {content!r}\n"
        f"  Скачано:   {download.content!r}"
    )


@pytest.mark.regression
@pytest.mark.mutating
def test_attachment_appears_in_list(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    upload = attachments_api.upload_attachment(
        client, task_id, "list-me.txt", b"data",
    )
    client.expect_status(upload, 200, 201)
    attachment_id = upload.json()["success"][0]["id"]

    resp = attachments_api.list_attachments(client, task_id)
    client.expect_status(resp, 200)
    ids = {a["id"] for a in resp.json()}
    assert attachment_id in ids


@pytest.mark.regression
@pytest.mark.mutating
def test_delete_attachment(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    upload = attachments_api.upload_attachment(
        client, task_id, "to-delete.txt", b"bye",
    )
    client.expect_status(upload, 200, 201)
    attachment_id = upload.json()["success"][0]["id"]

    resp = attachments_api.delete_attachment(client, task_id, attachment_id)
    client.expect_status(resp, 200, 204)

    check = attachments_api.download_attachment(client, task_id, attachment_id)
    client.expect_status(check, 404)



@pytest.mark.regression
@pytest.mark.mutating
def test_reader_sees_but_cannot_delete(
    client, second_user, project_factory, task_factory,
):
    project_id = project_factory()
    task_id = task_factory(project_id)

    upload = attachments_api.upload_attachment(
        client, task_id, "reader-view.txt", b"read-only content",
    )
    client.expect_status(upload, 200, 201)
    attachment_id = upload.json()["success"][0]["id"]


    _share_with(client, project_id, _username(second_user), permission=0)


    list_resp = attachments_api.list_attachments(second_user, task_id)
    second_user.expect_status(list_resp, 200)


    download = attachments_api.download_attachment(second_user, task_id, attachment_id)
    second_user.expect_status(download, 200)
    assert download.content == b"read-only content"


    delete_resp = attachments_api.delete_attachment(second_user, task_id, attachment_id)
    second_user.expect_status(delete_resp, 403)


@pytest.mark.regression
@pytest.mark.mutating
def test_stranger_cannot_download(
    client, second_user, project_factory, task_factory,
):
    project_id = project_factory()
    task_id = task_factory(project_id)

    upload = attachments_api.upload_attachment(
        client, task_id, "secret.txt", b"private data",
    )
    client.expect_status(upload, 200, 201)
    attachment_id = upload.json()["success"][0]["id"]


    download = attachments_api.download_attachment(second_user, task_id, attachment_id)
    second_user.expect_status(download, 403, 404)



@pytest.mark.regression
@pytest.mark.mutating
def test_upload_empty_file(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    content = b""

    upload = attachments_api.upload_attachment(client, task_id, "empty.bin", content)
    client.expect_status(upload, 200, 201)
    attachment_id = upload.json()["success"][0]["id"]

    download = attachments_api.download_attachment(client, task_id, attachment_id)
    client.expect_status(download, 200)
    assert download.content == b"", (
        f"Ожидается пустое тело, получено {download.content!r}"
    )


@pytest.mark.regression
@pytest.mark.mutating
def test_upload_cyrillic_filename(client, project_factory, task_factory):
    project_id = project_factory()
    task_id = task_factory(project_id)

    filename = "тестовый файл с кириллицей.txt"
    content = "тестовые данные".encode("utf-8")

    upload = attachments_api.upload_attachment(client, task_id, filename, content)
    client.expect_status(upload, 200, 201)


    body = upload.json()
    attachment = body["success"][0]
    attachment_id = attachment["id"]


    assert attachment["file"]["name"] == filename, (
        f"Имя файла не совпадает: "
        f"отправлено {filename!r}, получено {attachment['file']['name']!r}"
    )


    download = attachments_api.download_attachment(client, task_id, attachment_id)
    client.expect_status(download, 200)
    assert download.content == content, (
        f"Содержимое с кириллицей не совпало: {download.content!r}"
)