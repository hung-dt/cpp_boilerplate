#------------------------------------------------------------------------------
#   Author: HungDT
#   Date  : 2025-04-22
#
#   Clang-Format instructions
#------------------------------------------------------------------------------

find_program(CPPCHECK_BIN NAMES cppcheck)

if(CPPCHECK_BIN)
  message(STATUS "Found: cppcheck")
  list(
        APPEND CMAKE_CXX_CPPCHECK
            "${CPPCHECK_BIN}"
            "--enable=all"
            "--enable=warning,performance,portability,information"
            "--inconclusive"
            "--check-config"
            "--force"
            "--inline-suppr"
            "--xml"
            "--output-file=${CMAKE_BINARY_DIR}/cppcheck.xml"
    )
endif()