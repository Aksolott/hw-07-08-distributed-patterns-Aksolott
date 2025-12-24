package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/sony/gobreaker"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	// TODO: нужно сгенерировать proto и импортировать его
	// pb "hw07/proto"
)

// TODO: Определите структуры из proto здесь (или сгенерируйте их)
// Для примера оставим заглушки
type DataRequest struct{ Payload string }
type DataResponse struct{ Message string }

func main() {
	serverAddr := os.Getenv("SERVER_ADDR")
	if serverAddr == "" {
		serverAddr = "localhost:50051"
	}

	conn, err := grpc.NewClient(serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	// Настройка Circuit Breaker
	cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
		Name:        "UnstableService",
		MaxRequests: 1, // Кол-во запросов в Half-Open
		Timeout:     30 * time.Second,
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			// TODO: Реализуйте логику срабатывания (например, > 5 ошибок)
			return /**/
		},
	})

	for {
		callWithResilience(cb, conn)
		time.Sleep(1 * time.Second)
	}
}

func callWithResilience(cb *gobreaker.CircuitBreaker, conn *grpc.ClientConn) {
	// Паттерн Retry
	// TODO: Оберните вызов ниже в цикл с Exponential Backoff

	_, err := cb.Execute(func() (interface{}, error) {
		// Паттерн Timeout
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		defer cancel()

		// TODO: Вызовите реальный gRPC метод

		return nil, fmt.Errorf("not implemented")
	})

	if err != nil {
		log.Printf("Request failed: %v", err)
	} else {
		log.Println("Request success")
	}
}
