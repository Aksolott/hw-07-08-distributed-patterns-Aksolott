import os
from grpc_tools import protoc

def generate_proto():
    # Пути относительно корня python проекта
    proto_dir = "../proto"  # При локальном запуске
    if not os.path.exists(proto_dir):
        proto_dir = "proto" # Внутри Docker

    out_dir = "src/generated"
    os.makedirs(out_dir, exist_ok=True)
    
    # Создаем __init__.py, чтобы это был пакет
    with open(f"{out_dir}/__init__.py", "w") as f:
        pass

    protoc.main((
        "",
        f"-I{proto_dir}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        f"{proto_dir}/service.proto",
    ))
    print(f"Proto generated in {out_dir}")

if __name__ == "__main__":
    generate_proto()
