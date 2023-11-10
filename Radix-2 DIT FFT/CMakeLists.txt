cmake_minimum_required(VERSION 3.0)

set(MODULE_NAME "_ece3210_lab07")
project(${MODULE_NAME})

# general setup
include_directories(include)
add_compile_options(-Wall -Wconversion -fPIC -O3)

# Find OpenMP package
find_package(OpenMP REQUIRED)

# build libraries
add_library(fft src/fft.c)

# Append OpenMP flags to the fft library
target_compile_options(fft PRIVATE ${OpenMP_C_FLAGS})

# start the python stuff
set(PYBIND11_PYTHON_VERSION 3.9 CACHE STRING "")
find_package(pybind11 REQUIRED)
pybind11_add_module(${MODULE_NAME} src/main.cpp)
target_link_libraries(${MODULE_NAME} PUBLIC fft m)

# Link OpenMP library
target_link_libraries(fft PRIVATE OpenMP::OpenMP_C)

# installation
install(TARGETS ${MODULE_NAME} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/python)

