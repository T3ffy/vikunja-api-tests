# Vikunja API Tests

![CI](https://github.com/T3ffy/vikunja-api-tests/actions/workflows/ci.yml/badge.svg?branch=main)

Каркас автотестов для API Vikunja на pytest + requests. Покрывает smoke-проверки
критических путей: доступность API, авторизация, получение текущего пользователя,
список проектов.

## Стек

- Python 3.12
- pytest
- requests
- GitHub Actions (CI)

## Структура проекта

    vikunja-api-tests/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml              # CI: push, pull_request
    ├── clients/
    │   ├── __init__.py
    │   ├── http_client.py          # HttpClient: base_url, timeout, get/post/put/delete
    │   └── auth.py                 # регистрация + логин
    ├── envs/
    │   └── local.env               # BASE_URL для локального стенда
    ├── tests/
    │   ├── __init__.py
    │   └── test_smoke.py           # 5 smoke-тестов
    ├── config.py                   # чтение envs/<stand>.env
    ├── conftest.py                 # --stand, фикстура client
    ├── pytest.ini                  # маркеры
    ├── requirements.txt
    └── README.md

## Установка

    git clone https://github.com/T3ffy/vikunja-api-tests
    cd vikunja-api-tests

    py -3.12 -m venv .venv
    .venv\Scripts\Activate.ps1          # Windows
    # source .venv/bin/activate         # Linux / macOS

    python -m pip install --upgrade pip
    pip install -r requirements.txt

## Запуск Vikunja локально

Vikunja поднимается в Docker. Нужен Docker Desktop.

    docker run -d --name vikunja-ci --user 0 -p 3456:3456 `
      -e VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/ `
      -e VIKUNJA_SERVICE_SECRET=ci-test-secret-minimum-32-characters-long `
      -e VIKUNJA_DATABASE_TYPE=sqlite `
      -e VIKUNJA_DATABASE_PATH=/tmp/vikunja.db `
      -e VIKUNJA_SERVICE_ENABLEREGISTRATION=true `
      --tmpfs /app/vikunja/files `
      --tmpfs /tmp `
      vikunja/vikunja:2.6.0

Проверка, что API отвечает:

    curl.exe -s http://localhost:3456/api/v1/info


Убрать контейнер:

    docker rm -f vikunja-ci



## Запуск тестов

    # Smoke - быстрые проверки
    pytest -m smoke --stand local -v

    # Smoke + regression
    pytest -m "smoke or regression" --stand local -v

    # Всё
    pytest --stand local -v

### Опция --stand

Стенд задаётся файлом `envs/<stand>.env`. По умолчанию `local`.

Добавить новый стенд:

1. Создать `envs/dev.env`:

        BASE_URL=https://dev.vikunja.example.com/api/v1

2. Запустить:

        pytest -m smoke --stand dev -v


## Маркеры

Маркер       - Что означает                                                 

- `smoke`      - Быстрые проверки критических путей: доступность, авторизация 
- `regression` - Полный набор функциональных тестов                           
- `mutating`   - Тесты, которые создают/меняют/удаляют данные                 
- `contract`   - Проверки контракта API: обязательные поля, типы, схемы       

В CI запускаются только `smoke` и `regression`. Маркеры `mutating` и `contract`
гоняются локально или в отдельном пайплайне.

## Что покрыто

Smoke-тесты (`tests/test_smoke.py`):

- `/info` отвечает и версия 2.6.0
- логин выдаёт токен
- `/user` возвращает того, кто вошёл
- список проектов доступен
- без токена `/user` не отдаётся

## CI

`.github/workflows/ci.yml` запускается на push и pull_request.

Что делает:

1. Поднимает Vikunja `2.6.0` как service-контейнер на порту 3456.
2. Ставит Python 3.12 и зависимости из `requirements.txt`.
3. Ждёт готовности API через curl (`/api/v1/info`), максимум 60 секунд.
4. Гоняет `pytest -m "smoke or regression" --stand local -v`.

Локально можно эмулировать то же самое:

    docker run -d --name vikunja-ci --user 0 -p 3456:3456 \
      -e VIKUNJA_SERVICE_ENABLEREGISTRATION=true \
      -e VIKUNJA_SERVICE_SECRET=ci-test-secret-minimum-32-characters-long \
      -e VIKUNJA_DATABASE_TYPE=sqlite \
      -e VIKUNJA_DATABASE_PATH=/tmp/vikunja.db \
      --tmpfs /app/vikunja/files \
      --tmpfs /tmp \
      vikunja/vikunja:2.6.0

    pytest -m "smoke or regression" --stand local -v


### `http_сlient`

Базовый HTTP-клиент. Хранит `base_url`, `timeout`, заголовки и токен.

- `get/post/put/delete(path, **kwargs)` - методы запросов.
- `set_token(token)` - устанавливает Bearer-токен для всех последующих запросов.
- `expect_status(response, *codes)` - проверяет статус-код; при несовпадении
  падает с сообщением, в котором есть метод, URL, ожидаемые коды,
  фактический код и первые 200 символов тела.

`expect_status` -  Когда тест падает, в трейсе видно, что именно пошло не так. Например, при rate limit Vikunja
возвращает 429, и в сообщении видно `{"message":"Too Many Requests"}`

### Фикстура `client`

    @pytest.fixture(scope="session")
    def client(stand: str) -> HttpClient:
        base_url = get_base_url(stand)
        http = HttpClient(base_url=base_url)
        register_and_login(http)
        return http

Один авторизованный клиент на весь прогон. `scope="session"` - потому что
Vikunja ограничивает частоту регистраций/

### `config.py` + `envs/`

`config.py` читает переменные из `envs/<stand>.env`. Формат - простые
`KEY=VALUE`, по строке на переменную. 

