import requests

class http_client:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self._token = None

    def set_token(self, token:str) -> None:
        self.token=token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        
    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(self._url(path), timeout=self.timeout, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.session.put(self._url(path), timeout=self.timeout, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)

    @staticmethod
    def expect_status(response: requests.Response, *expected_codes: int) -> None:
        if response.status_code not in expected_codes:
            body_snippet = response.text[:200] if response.text else "<пустое тело>"
            raise AssertionError(
                f"Неожиданный статус-код\n"
                f"  Метод:   {response.request.method}\n"
                f"  URL:     {response.request.url}\n"
                f"  Ожидаемо: {expected_codes}\n"
                f"  Получено: {response.status_code}\n"
                f"  Тело:    {body_snippet}"
            )