# Vikunja & Toolshop API Tests
![CI](https://github.com/T3ffy/vikunja-api-tests/actions/workflows/ci.yml/badge.svg?branch=main)
Учебный проект автотестов на Python + pytest + requests + Schemathesis. Покрывает API Vikunja (проекты, задачи, вложения, шеринг) и Toolshop (авторизация и роли). 

## Зачем этот проект

Отработка на учебных стендах тех же паттернов, что и в рабочем
репозитории:

- HTTP-клиент с `base_url`, `timeout`, `set_token`, `expect_status`;
- авторизация через фикстуры;
- выбор стенда через `--stand` + `envs/<stand>.env`;
- фабрики с автоуборкой через `yield`;
- contract-тестирование через Schemathesis;
- работа с двумя стендами одного API (clean / with-bugs);
- CI на GitHub Actions с артефактами.

## Как поднять и запустить

### Требования

- Python 3.12
- Docker Desktop (для Vikunja)
- Git

### Клонирование и установка

    git clone <https://github.com/T3ffy/vikunja-api-tests.git>
    cd vikunja-api-tests
    py -3.12 -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    playwright install chromium

### Vikunja локально

    docker run -d --name vikunja-ci --user 0 -p 3456:3456 `
      -e VIKUNJA_SERVICE_PUBLICURL=http://localhost:3456/ `
      -e VIKUNJA_SERVICE_SECRET=ci-test-secret-minimum-32-characters-long `
      -e VIKUNJA_DATABASE_TYPE=sqlite `
      -e VIKUNJA_DATABASE_PATH=/tmp/vikunja.db `
      -e VIKUNJA_SERVICE_ENABLEREGISTRATION=true `
      --tmpfs /app/vikunja/files --tmpfs /tmp `
      vikunja/vikunja:2.6.0

Проверка:

    curl.exe -s http://localhost:3456/api/v1/info
    # {"version":"v2.6.0",...}

### Прогон тестов

    # Smoke — быстрые проверки
    pytest -m smoke --stand local -v

    # Smoke + regression
    pytest -m "smoke or regression" --stand local -v

    # Всё, кроме contract и Toolshop
    pytest -m "smoke or regression" --stand local -v `
      --ignore=tests/contract --ignore=tests/toolshop

    # Contract-тесты (только локально, шумный прогон)
    pytest tests/contract/ -v --stand local

    # Toolshop — чистый стенд
    pytest tests/toolshop/ -v --stand pst-clean

    # Toolshop — стенд с багами
    pytest tests/toolshop/ -v -rx --stand pst-bugs

### HTML-отчёт

    pytest -m "smoke or regression" --stand local -v `
      --html=reports/report.html --self-contained-html

    start reports\report.html

### В CI

CI запускается на push и pull_request в `main`. Открыть вкладку Actions репозитория, скачать артефакт `pytest-html-report` после прогона.

## Структура

    vikunja-api-tests/
    ├── .github/workflows/ci.yml       # CI
    ├── api/                            # обёртки над эндпоинтами Vikunja
    │   ├── projects.py
    │   ├── tasks.py
    │   ├── teams.py
    │   ├── shares.py
    │   └── attachments.py
    ├── clients/                        # низкоуровневый клиент
    │   ├── http_client.py              # HttpClient
    │   └── auth.py                     # register_and_login
    ├── envs/                           # стенды
    │   ├── local.env
    │   ├── pst-clean.env
    │   └── pst-bugs.env
    ├── tests/                          # тесты
    │   ├── conftest.py
    │   ├── test_smoke.py
    │   ├── test_projects.py
    │   ├── test_task.py
    │   ├── test_shares.py
    │   ├── test_teams.py
    │   ├── test_attachments.py
    │   ├── contract/                   # contract-тесты Schemathesis
    │   │   ├── test_contract_get.py
    │   │   └── test_known_bugs.py
    │   └── toolshop/                   # Toolshop
    │       ├── conftest.py
    │       └── test_auth_roles.py
    ├── config.py                       # чтение envs/<stand>.env
    ├── conftest.py                     # --stand, общие фикстуры
    ├── pytest.ini
    └── README.md

## Матрица прав Vikunja

Проверено на Vikunja 2.6.0. Уровни доступа:

| right | Что значит |
|---|---|
| 0 | Read only |
| 1 | Read + Write |
| 2 | Admin (управляет шерингом) |

Что может каждый уровень в чужом проекте:

| Кто | Прочитать | Создать задачу | Изменить проект | Удалить проект | Расшарить дальше |
|---|---|---|---|---|---|
| Владелец | да | да | да | да | да |
| right=0 | да | нет (403) | нет (403) | нет (403) | нет (403) |
| right=1 | да | да | да | нет (403) | нет (403) |
| right=2 | да | да | да | да (200) | да |


Admin получает все права владельца, кроме смены владельца.

## Дефекты

- **VK-001 / VK-002**: PUT на `webhooks/events` и `buckets/tasks`
  возвращает `400` вместо `405` (Vikunja).
- **VK-003**: `/avatar/{username}` отдаёт `image/svg+xml` вместо
  `application/octet-stream` (ошибка спецификации).
- **TS-001**: BOLA - customer читает чужой профиль (Toolshop pst-bugs).
- **TS-002**: Excessive Data Exposure - `password`, `role` в ответе
  `/users/{id}` (Toolshop pst-bugs).
- **TS-003**: BFLA - customer удаляет бренд (Toolshop pst-bugs).

## Что бы сделал дальше

1. Расширил contract-тесты добавил бы к GET ещё POST/PUT/DELETE.
2. Перешёл на Allure для более наглядных отчётов в CI.
3. Добавил ночной-прогон regression-тестов по расписанию.
4. Покрыл Toolshop большим набором тестов.
5. Ускорил CI через кэш `pip`, параллельные job.
6. Добавил UI тесты с Page Object
7. Дабавил прогон с уведомлением в Telegram при падении.