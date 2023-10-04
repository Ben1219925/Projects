cmake_minimum_required(VERSION 3.0)

set(MODULE_NAME "_ece3210_lab01")
project(${MODULE_NAME})

# general setup
include_directories(include)
add_compile_options(-Wall -Wconversion -fPIC -O3)
set(CMAKE_CXX_FLAGS "-flto=auto")

# build libraries
add_library(integrate src/integrate.c)

# start the python stuff
set(PYBIND11_PYTHON_VERSION 3.9 CACHE STRING "")
find_package(pybind11 REQUIRED)
pybind11_add_module(${MODULE_NAME} src/main.cpp)
target_link_libraries(${MODULE_NAME} PUBLIC integrate m)

# installation
install(TARGETS ${MODULE_NAME} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/python)

