cmake_minimum_required(VERSION 3.12)

project(adios2-performance-testing LANGUAGES NONE)

function(find_exec_in_env VAR EXE_NAME)
  message(STATUS "Locating ${EXE_NAME}...")
  if(NOT ${VAR})
    execute_process(
      COMMAND
        "${PROJECT_SOURCE_DIR}/common/env-exec.sh"
          "${ENV_SETUP}" which "${EXE_NAME}"
      RESULT_VARIABLE ret
      OUTPUT_VARIABLE out
      ERROR_QUIET
      OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    if(NOT ret EQUAL 0)
      set(${VAR} "${VAR}-NOTFOUND" CACHE FILEPATH "" FORCE)
      message(FATAL_ERROR "${VAR}-NOTFOUND")
    else()
      set(${VAR} "${out}" CACHE FILEPATH "" FORCE)
    endif()
  endif()
  message(STATUS "Locating ${EXE_NAME}... ${${VAR}}")
endfunction()

set(MACHINE "local" CACHE STRING "Use a pre-defined machine profile")
set(SWEEP_GROUP "" CACHE STRING "The cheetah sweep group to use")
set(ENV_SETUP "ENV_SETUP-NOTFOUND" CACHE FILEPATH "")
mark_as_advanced(ENV_SETUP)
set(TEST_OUTPUT_BASE_DIR
  "${PROJECT_BINARY_DIR}/test-output" CACHE PATH "Test output directory"
)

find_program(PYTHON_EXECUTABLE python3)
if(NOT PYTHON_EXECUTABLE)
  message(FATAL_ERROR "Unable to locate python3 in the current environment")
endif()

include(CTest)
set(BUILD_TESTING ON CACHE BOOL "" FORCE)
mark_as_advanced(BUILD_TESTING)
enable_testing()

option(ENABLE_XGC_RESTART "Enable the XGC Restart test" TRUE)
if(ENABLE_XGC_RESTART)
  add_subdirectory(xgc-restart)
endif()
