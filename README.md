# Мини-система турниров

Это минимальное backend-приложение на FastAPI для управления турнирами и регистрации игроков в них. Приложение использует асинхронную работу с базой данных через SQLAlchemy 2.0 и Alembic для миграций.

## Технологии

- **Python 3.12+**
- **FastAPI** - для создания REST API
- **SQLAlchemy 2.0+ (Async)** - для работы с базой данных PostgreSQL
- **Alembic** - для управления миграциями базы данных
- **Pydantic** - для валидации данных
- **PostgreSQL** - база данных
- **Docker + Docker Compose** - для контейнеризации и управления сервисами
- **Mypy** - для статической типизации
- **Ruff** - для линтинга
- **Black** - для автоматического форматирования кода
- **Pytest** - для тестирования


## Запуск проекта

Для локального запуска проекта следуйте этим шагам:

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/timurxboy/tournament.git
cd tournament
```

### 2. Создайте файл .env и настройте переменные окружения
Скопируйте файл .env.example в .env и отредактируйте переменные окружения для вашего окружения.

```
MODE=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST= 
DB_PORT=

TEST_DB_NAME=
TEST_DB_USER=
TEST_DB_PASSWORD=
TEST_DB_HOST=
TEST_DB_PORT=
```
MODE - принимает "TEST" или "DEV"

DB_HOST и TEST_DB_HOST - предпочетается написать localhost так-как они нужны для доступа из вне контейнера

DB_PORT и TEST_DB_PORT - предпочетается написать 5432 и 5433 соответсвенно так-как они нужны для доступа из вне контейнера


### 3. Запустите контейнеры Docker
Запустите все сервисы с помощью Docker Compose:
```
docker-compose up --build
```


### 4. Примените миграции базы данных
После запуска контейнеров, примените миграции:

```
docker-compose exec app poetry run alembic upgrade head
```

### 5. Откройте документацию API
После запуска сервера, документация API будет доступна по адресу:
```
http://localhost:8000/docs
```


## API
### 1. Создание турнира
POST /tournaments

Создаёт новый турнир.

Запрос:
```
{
  "name": "Weekend Cup",
  "max_players": 8,
  "start_at": "2025-06-23T17:40:00"
}
```

Ответ:
```
{
  "id": 1,
  "name": "Weekend Cup",
  "max_players": 8,
  "start_at": "2025-06-23T17:40:00Z"
}
```

### 2. Регистрация игрока
POST /tournaments/{tournament_id}/register

Регистрирует игрока в турнир.

Запрос:
```
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

Ответ:
```
{
  "id": 1,
  "name": "Weekend Cup",
  "max_players": 8,
  "start_at": "2025-06-23T17:40:00Z",
  "registered_players": 1
}
```


### 3. Список турниров с пагинацией и фильтрацией
GET /tournaments

Получает список всех турниров с возможностью пагинации и фильтрации.

Параметры запроса:
- page — номер страницы для пагинации (по умолчанию 1)
- per_page — количество турниров на странице (по умолчанию 10)
- order_by — направление сортировки: asc или desc (по умолчанию desc)
- sort_by — поле для сортировки: id, name (по умолчанию id)

Получает список зарегистрированных игроков.

Пример запроса:
```
GET /tournaments?page=1&per_page=10&order_by=asc&sort_by=id
```

Ответ:
```
{
  "pages": 1,
  "values": [
    {
      "id": 1,
      "name": "Weekend Cup",
      "max_players": 8,
      "start_at": "2025-06-23T17:40:00+00:00",
      "registered_players": 1
    }
  ]
}
```

## Тестирование

Для запуска тестов:
```
docker-compose exec app poetry run pytest
```

## Линтинг и форматирование

Запуск mypy:
```
docker-compose exec app poetry run mypy ./app
```

Запуск black:
```
docker-compose exec app poetry run black ./app
```

Запуск ruff:
```
docker-compose exec app poetry run ruff check ./app
```


## Стандарты кода

- Код должен соответствовать стандартам линтинга (Ruff) и форматирования (Black).

- Строгая типизация с использованием Mypy.

- Асинхронная работа с базой данных через SQLAlchemy 2.0+.


## Заключение
Этот проект реализует простую систему турниров с возможностью создания турниров, регистрации игроков, получения пагинированного списка всех турниров. Все запросы обрабатываются асинхронно, с использованием лучших практик разработки для FastAPI и PostgreSQL.