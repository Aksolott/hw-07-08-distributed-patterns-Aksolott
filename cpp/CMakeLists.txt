cmake_minimum_required(VERSION 3.13)
project(resilience_hw CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Находим пакет userver. 
# В Docker-образе ghcr.io/userver-framework/ubuntu-22.04-userver-base он уже установлен.
find_package(userver COMPONENTS core grpc REQUIRED)

# Макрос userver_add_grpc_library генерирует асинхронные клиенты и сервисы
userver_add_grpc_library(resilience-proto
    PROTOS ../proto/service.proto
    SOURCE_PATH ../proto
)

add_executable(resilience_client
    src/main.cpp
    src/service.cpp
    src/service.hpp
)

target_link_libraries(resilience_client
    PRIVATE
    resilience-proto
    userver::core
    userver::grpc
)

target_include_directories(resilience_client PRIVATE src)

file(COPY configs/config.yaml DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
