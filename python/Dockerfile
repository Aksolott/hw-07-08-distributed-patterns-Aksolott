FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY . .

RUN uv sync --frozen
RUN mkdir -p src/generated
RUN uv run python src/codegen.py

# ФИКС: Исправляем импорты в сгенерированном файле
RUN sed -i 's/import service_pb2 as service__pb2/from generated import service_pb2 as service__pb2/' src/generated/service_pb2_grpc.py

CMD ["uv", "run", "python", "src/client.py"]