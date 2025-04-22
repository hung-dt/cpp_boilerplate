#------------------------------------------------------------------------------
#   Author: HungDT
#   Date  : 2025-04-22
#
#   Main CMake project file
#------------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.23.0)

project(cpp_template
    VERSION 1.0.0
    DESCRIPTION "C++ project template"
    LANGUAGES C CXX)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

#------------------------------------------------------------------------------
# Import cmake modules
#------------------------------------------------------------------------------

include(ClangFormat)
include(CppCheck)

#------------------------------------------------------------------------------
# External C++ libraries (these may go into specific modules)
#------------------------------------------------------------------------------

find_package(fmt CONFIG REQUIRED)

#------------------------------------------------------------------------------
# Project cmake options
#------------------------------------------------------------------------------

option(BUILD_SHARED_LIBS "Build shared libraries" ON)
option(BUILD_TESTS "Build tests" OFF)
option(BUILD_EXAMPLES "Build sample programs" OFF)

#------------------------------------------------------------------------------
# Other project's CMakeLists.txt
#------------------------------------------------------------------------------

add_subdirectory(src)

# examples
if (BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# tests
if (BUILD_TESTS)
    add_subdirectory(tests)
endif()
