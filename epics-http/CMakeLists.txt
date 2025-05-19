cmake_minimum_required (VERSION 3.22)
project(cprClientTest)

# Generate compile_commands.json for LSP's
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Libraries I build from source are in ~/.local
list(APPEND CMAKE_PREFIX_PATH "$ENV{HOME}/.local")

find_package(OpenSSL REQUIRED)
find_package(cpr CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)

add_executable(cprClientTest main.cpp)
target_link_libraries(cprClientTest PRIVATE OpenSSL::SSL cpr::cpr nlohmann_json::nlohmann_json)
