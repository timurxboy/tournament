# Используем официальный Python образ
FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && \
    apt-get clean

# Устанавливаем рабочую директорию
RUN mkdir /tournament
WORKDIR /tournament

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"


# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY ./pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Копируем содержимое проекта
COPY . .

CMD ["uvicorn", "app.main:app", "--reload"]