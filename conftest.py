import pytest

from config import get_base_url
from clients.http_client import http_client
from clients.auth import register_and_login


def pytest_addoption(parser):
    parser.addoption(
        "--stand",
        default="local",
    )


@pytest.fixture(scope="session")
def stand(request) -> str:
    return request.config.getoption("--stand")


@pytest.fixture
def client(stand: str) -> http_client:
    base_url = get_base_url(stand)
    http = http_client(base_url=base_url)
    register_and_login(http)
    return http

@pytest.fixture(scope="session")
def stand(request) -> str:
    return request.config.getoption("--stand")

@pytest.fixture (scope="session")
def client(stand:str) -> http_client:
    base_url=get_base_url(stand)
    http= http_client(base_url=base_url)
    register_and_login(http)
    return http