package main

import (
	"context"
	"log"
	"math/rand"
	"net"
	"os"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"

	pb "hw07/proto" 
)

type server struct {
	pb.UnimplementedUnstableServiceServer
}

func (s *server) ProcessData(ctx context.Context, req *pb.DataRequest) (*pb.DataResponse, error) {
	chaosMode := os.Getenv("CHAOS_MODE") == "true"

	if chaosMode {
		// Генерируем число от 0.0 до 1.0
		r := rand.Float64()

		// 1. Latency Injection (20% случаев)
		if r < 0.2 {
			log.Printf("[Chaos] Simulating network lag (5s) for payload: %s", req.Payload)
			time.Sleep(5 * time.Second)
		} else if r < 0.4 {
			// 2. Fault Injection (20% случаев)
			log.Printf("[Chaos] Simulating failure for payload: %s", req.Payload)
			return nil, status.Error(codes.Unavailable, "Service temporarily unavailable (Chaos Monkey)")
		}
	}

	log.Printf("Successfully processed: %s", req.Payload)
	return &pb.DataResponse{
		Success: true,
		Message: "Processed: " + req.Payload,
	}, nil
}

func main() {
	// Инициализация рандома (для старых версий Go, в новых не обязательно, но полезно)
	rand.Seed(time.Now().UnixNano())

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterUnstableServiceServer(s, &server{})

	log.Printf("Go Server listening on :50051 (Chaos Mode: %s)", os.Getenv("CHAOS_MODE"))
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
