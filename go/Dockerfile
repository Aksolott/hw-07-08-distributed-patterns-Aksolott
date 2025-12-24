FROM golang:1.21-alpine AS builder

WORKDIR /app

# Устанавливаем protoc
RUN apk add --no-cache protobuf-dev

# Копируем зависимости
COPY go/go.mod go/go.sum ./
RUN go mod download

# Копируем исходники и proto
COPY go/ ./
COPY proto/ ../proto/

# TODO: Добавьте шаг генерации proto (protoc)

# Сборка
RUN go build -o client ./client/main.go
RUN go build -o server ./server/main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/client .
COPY --from=builder /app/server .

CMD ["./client"]
