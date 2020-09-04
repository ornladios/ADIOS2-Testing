set(TEST_PROFILE "xgc-restart")
set(TEST_OUTPUT_DIR "${TEST_OUTPUT_BASE_DIR}/${TEST_PROFILE}")

set(XGC_ENV_SETUP
  "${CMAKE_CURRENT_SOURCE_DIR}/env-setup/env_setup_${MACHINE}.sh"
  CACHE FILEPATH "Environment setup script"
)
mark_as_advanced(XGC_ENV_SETUP)
if(NOT ENV_SETUP)
  if(EXISTS "${XGC_ENV_SETUP}")
    set(ENV_SETUP "${XGC_ENV_SETUP}")
  else()
    set(ENV_SETUP "${CMAKE_CURRENT_SOURCE_DIR}/common/empty-env.sh")
  endif()
endif()

message("Using ENV_SETUP=\"${ENV_SETUP}\"")
find_exec_in_env(EXE_CHEETAH cheetah)
find_exec_in_env(EXE_TAU_EXEC tau_exec)
find_exec_in_env(EXE_BPLS bpls)
find_exec_in_env(EXE_IOTEST adios2_iotest)

#######################################
# Campaign and script setup
#######################################

message("Generating ${TEST_PROFILE} test scripts in \"${TEST_OUTPUT_DIR}\"")

if(EXISTS "${TEST_OUTPUT_DIR}")
  message(STATUS "  Cleaning up old test data")
  file(REMOVE_RECURSE "${TEST_OUTPUT_DIR}")
endif()

message(STATUS "  Generating campaing configuration")
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/campaign.py.in"
  "${TEST_OUTPUT_DIR}/campaign.py"
  @ONLY
)

message(STATUS "  Generating run scripts")
configure_file(
  "${PROJECT_SOURCE_DIR}/common/cheetah-run-and-wait.sh.in"
  "${TEST_OUTPUT_DIR}/cheetah-run-and-wait.sh"
  @ONLY
)
configure_file(
  "${PROJECT_SOURCE_DIR}/common/cheetah-group-stats.sh.in"
  "${TEST_OUTPUT_DIR}/cheetah-group-stats.sh"
  @ONLY
)

message(STATUS "  Generating full cheetah campaign")
set(ENV{PYTHONPATH} "${CMAKE_CURRENT_SOURCE_DIR}:$ENV{PYTHONPATH}")
execute_process(
  COMMAND "${PROJECT_SOURCE_DIR}/common/env-exec.sh" "${ENV_SETUP}"
    cheetah create-campaign
      -a "${CMAKE_CURRENT_SOURCE_DIR}"
      -e "${TEST_OUTPUT_DIR}/campaign.py"
      -m ${MACHINE}
      -o "${TEST_OUTPUT_DIR}"
  WORKING_DIRECTORY "${TEST_OUTPUT_DIR}"
)

# Submit / run the experiments as a build target
add_custom_target(${TEST_PROFILE}-run-and-wait ALL
  COMMAND "${TEST_OUTPUT_DIR}/cheetah-run-and-wait.sh"
)

# Collect and analyze the results as another build target
add_custom_target(${TEST_PROFILE}-generate-reports ALL
  COMMAND "${PROJECT_SOURCE_DIR}/common/env-exec.sh" "${ENV_SETUP}"
    cheetah generate-report "${TEST_OUTPUT_DIR}"
      -u "${PROJECT_SOURCE_DIR}/${TEST_PROFILE}/parse_timings.py"
)
add_dependencies(${TEST_PROFILE}-generate-reports ${TEST_PROFILE}-run-and-wait)

# Collect per-group statistics
file(GLOB LS LIST_DIRECTORIES TRUE "${TEST_OUTPUT_DIR}/$ENV{USER}/*")
foreach(RGD IN LISTS LS)
  if(NOT IS_DIRECTORY "${RGD}")
    continue()
  endif()
  get_filename_component(RG "${RGD}" NAME)
  message(STATUS "Adding test group: ${TEST_PROFILE}-${RG}")
  add_test(NAME ${TEST_PROFILE}-${RG}
    COMMAND "${TEST_OUTPUT_DIR}/cheetah-group-stats.sh" "${RGD}"
  )
endforeach()
