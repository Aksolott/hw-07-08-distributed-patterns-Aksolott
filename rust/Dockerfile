FROM rust:1.75 as builder

WORKDIR /app

# Копируем манифесты
COPY rust/Cargo.toml rust/Cargo.lock ./

# Копируем исходники и proto
COPY rust/src ./src
COPY rust/build.rs .
COPY proto ../proto

# Сборка
RUN cargo build --release --bin server --bin client

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/server ./server
COPY --from=builder /app/target/release/client ./client
CMD ["./client"]
