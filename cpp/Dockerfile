# Используем готовый образ с userver (или собираем свой, что долго)
FROM ghcr.io/userver-framework/ubuntu-22.04-userver-base:latest

WORKDIR /app

# Копируем исходники
COPY cpp/ .
COPY proto/ ../proto/

# Сборка через CMake
RUN mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc)

CMD ["./build/resilience_client"]
