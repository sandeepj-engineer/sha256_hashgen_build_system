cmake_minimum_required(VERSION 3.10)
project(CodegenBuild C)

# Include generated sources
set(CODEGEN_DIR "${CMAKE_SOURCE_DIR}/_builds/_out")

# Recursively find all .c files
file(GLOB_RECURSE CODEGEN_SOURCES "${CODEGEN_DIR}/*.c")

# Include headers
include_directories(${CODEGEN_DIR})

# Create executable only if there are sources
if(CODEGEN_SOURCES)
    add_executable(codegen_app ${CODEGEN_SOURCES})
else()
    message(FATAL_ERROR "No source files found in ${CODEGEN_DIR}")
endif()
