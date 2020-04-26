cmake_minimum_required(VERSION 3.15)
project(boilerplate VERSION 0.1.0)

#------------------------------------------------------------------------------
# Set default build type
#------------------------------------------------------------------------------
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to 'RelWithDebInfo' as non was specified")
    set(CMAKE_BUILD_TYPE RelWithDebInfo
        CACHE STRING "Choose the type of build." FORCE)

    # set possible values of build type for cmake-gui, ccmake
    set_property(CACHE CMAKE_BUILD_TYPE
        PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

#------------------------------------------------------------------------------
# Compiler configs
#------------------------------------------------------------------------------
if (NOT CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Wall -Wextra")
option(WARNINGS_AS_ERRORS "Treat compiler warnings as errors" FALSE)
if (WARNINGS_AS_ERRORS)
    set(CMAKE_CXX_FLAGS "${CMAXE_CXX_FLAGS} -Werror")
endif()

#------------------------------------------------------------------------------
# General cmake settings
#------------------------------------------------------------------------------
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/_bin/$<CONFIG>)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/_lib/$<CONFIG>)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/_lib/$<CONFIG>)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

#------------------------------------------------------------------------------
# External C++ libraries
#------------------------------------------------------------------------------

# sfml
set(SFML_DIR "D:/Dev/opt/lib/cmake/SFML")
find_package(SFML 2.5 COMPONENTS graphics window system network audio REQUIRED)

# imgui-sfml
set(ImGui-SFML_DIR "D:/Dev/opt/lib/cmake/ImGui-SFML")
find_package(ImGui-SFML REQUIRED)

# spdlog
set(spdlog_DIR "D:/Dev/opt/lib/cmake/spdlog")
find_package(spdlog REQUIRED)

# docopt
set(docopt_DIR "D:/Dev/opt/lib/cmake/docopt")
find_package(docopt COMPONENTS CXX REQUIRED)

# catch2
find_package(Catch2 REQUIRED)

# doctest
find_package(doctest REQUIRED)

# cxxopts
find_package(cxxopts CONFIG REQUIRED)

# SDL
set(SDL2_DIR "D:/Dev/opt/SDL2-2.0.12/x86_64-w64-mingw32/lib/cmake/SDL2")
find_package(SDL2 REQUIRED)

#------------------------------------------------------------------------------
# Project cmake options
#------------------------------------------------------------------------------
option(BUILD_SHARED_LIBS "Build shared libraries (*.so/*.dll)" ON)
option(BUILD_TESTS "Build tests" OFF)
option(BUILD_EXAMPLES "Build sample programs" ON)

#------------------------------------------------------------------------------
# Other CMakeLists.txt
#------------------------------------------------------------------------------

# src
add_subdirectory(src)

# examples
if (BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# tests
if (BUILD_TESTS)
    add_subdirectory(tests)
endif()
