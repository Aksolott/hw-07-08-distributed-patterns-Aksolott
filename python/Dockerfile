# Используем официальный образ с uv
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# 1. Копируем файлы проекта
COPY python/pyproject.toml python/uv.lock ./
# Копируем proto из корня репозитория (благодаря context: . в docker-compose)
COPY proto/ ./proto/ 
COPY python/src/ ./src/

# 2. Устанавливаем зависимости
RUN uv sync --frozen

# 3. Генерируем gRPC код
RUN uv run python src/codegen.py

# 4. Запуск (переопределяется в docker-compose)
CMD ["uv", "run", "python", "src/client.py"]
