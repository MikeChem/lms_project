# Dockerfile

# Базовый образ Python
FROM python:3.13-slim

# Установка зависимостей системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        postgresql \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml .
COPY poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем исходники
COPY . .

# Собираем статику (если используется)
RUN python manage.py collectstatic --noinput

# Порт, который слушает Django
EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]