# Meteo API

Описание проекта

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- PyJWT
- Pytest

## Возможности

- Регистрация
- Авторизация
- Добавление города
- Получение прогноза
- Получение списка городов
- Unit и integration тесты

## Запуск
```shell
git clone https://github.com/alexandrwrks/meteo

uv venv

uv sync

alembic upgrade head

uvicorn app.main:app --port 8000 --host 127.0.0.1 --reload
```

## Запуск тестов
```shell
pytest
```

## API

![Swagger](docs/swagger.png)


## Тесты

![Tests](docs/tests.png)