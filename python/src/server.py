import time
import random
import os
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc

class UnstableService(service_pb2_grpc.UnstableServiceServicer):
    def ProcessData(self, request, context):
        chaos_mode = os.getenv("CHAOS_MODE", "false").lower() == "true"
        
        if chaos_mode:
            rand_val = random.random()
            
            # 1. Latency injection (20%)
            if rand_val < 0.2:
                time.sleep(5)
            
            # 2. Fault injection (20%)
            elif rand_val < 0.4:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("Service is temporarily unavailable (Chaos)")
                return service_pb2.DataResponse()

        return service_pb2.DataResponse(success=True, message=f"Processed: {request.payload}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_UnstableServiceServicer_to_server(UnstableService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
