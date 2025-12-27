import grpc
import time
import os
import sys

# Добавляем путь к сгенерированным файлам
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import service_pb2
import service_pb2_grpc

# Импорт библиотек для паттернов
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit

# Адрес сервера из ENV
SERVER_ADDR = os.getenv("SERVER_ADDR", "localhost:50051")

class ResilienceClient:
    def __init__(self):
        self.channel = grpc.insecure_channel(SERVER_ADDR)
        self.stub = service_pb2_grpc.UnstableServiceStub(self.channel)

    # TODO: Задача 2.3. Настройте Circuit Breaker
    # Если N ошибок подряд -> состояние OPEN
    # TODO: Задача 2.2. Настройте Retry
    def send_request(self, payload: str):
        print(f"[Client] Sending: {payload}")
        
        # TODO: Задача 2.1. Добавьте Timeout (2 секунды)
        return self.stub.ProcessData(
            service_pb2.DataRequest(payload=payload),
            timeout=2.0 
        )

def main():
    client = ResilienceClient()
    
    # Бесконечный цикл запросов
    i = 0
    while True:
        try:
            resp = client.send_request(f"ping_{i}")
            print(f"[Client] Success: {resp.message}")
        except Exception as e:
            print(f"[Client] Error: {e}")
        
        i += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
