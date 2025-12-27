import grpc
import time
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from circuitbreaker import circuit, CircuitBreakerError
import os

# Импорты generated
from generated import service_pb2
from generated import service_pb2_grpc


# ==================== CIRCUIT BREAKER ====================
@circuit(failure_threshold=5, recovery_timeout=30)
def make_request_with_circuit_breaker(stub, request):
    """Функция обернутая в Circuit Breaker"""
    # Таймаут 2 секунды
    context = grpc.ClientContext(timeout=2)

    try:
        response = stub.ProcessData(request, context=context)
        return response
    except grpc.RpcError as e:
        raise e


# ==================== RETRY + TIMEOUT ====================
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(grpc.RpcError),
)
def make_resilient_request(stub, request, attempt_count):
    """Основная функция с Retry и Timeout"""

    try:
        response = make_request_with_circuit_breaker(stub, request)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Успех: {response.message}")
        return response

    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⏰ Таймаут (2с) превышен")
        elif e.code() == grpc.StatusCode.UNAVAILABLE:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔌 Сервер недоступен")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ошибка gRPC: {e.code()}")

        # Для retry
        if attempt_count < 3:
            delay = 2 ** attempt_count  # 1, 2, 4 секунды
            print(f"  ↳ Попытка {attempt_count + 1}/3 через {delay}с...")

        raise e

    except CircuitBreakerError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ Circuit Breaker OPEN - запросы блокируются")
        raise e


# ==================== MAIN ====================
def run_client():
    """Основная функция клиента"""

    server_addr = os.getenv('SERVER_ADDR', 'server:50051')
    print(f"🔗 Подключаемся к серверу: {server_addr}")
    print(f"⚙️  Режим работы:")
    print(f"   • Таймаут: 2 секунды")
    print(f"   • Retry: 3 попытки с exponential backoff (1s, 2s, 4s)")
    print(f"   • Circuit Breaker: 5 ошибок → OPEN, через 30s → HALF-OPEN")
    print("-" * 50)

    channel = grpc.insecure_channel(server_addr)
    stub = service_pb2_grpc.UnstableServiceStub(channel)

    request_count = 0
    while True:
        request_count += 1
        request = service_pb2.DataRequest(payload=f"Запрос #{request_count}")

        print(f"\n📨 Отправка {request.payload}...")

        attempt = 0
        try:
            # Имитируем retry вручную для лучшего контроля
            while attempt < 3:
                try:
                    response = make_request_with_circuit_breaker(stub, request)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Успех: {response.message}")
                    break
                except grpc.RpcError as e:
                    attempt += 1
                    if attempt < 3:
                        delay = 2 ** (attempt - 1)  # 1, 2, 4 секунды
                        print(f"  ↳ Попытка {attempt}/3 через {delay}с...")
                        time.sleep(delay)
                    else:
                        print(f"   💥 Все 3 попытки исчерпаны")
                        raise
        except CircuitBreakerError:
            print(f"   ⚡ Запрос заблокирован Circuit Breaker")
        except Exception as e:
            print(f"   💥 Ошибка: {type(e).__name__}")

        time.sleep(1)


if __name__ == '__main__':
    run_client()