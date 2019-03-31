configure_file(adios2.xml adios2.xml COPYONLY)
configure_file(dump.sh.in dump.sh @ONLY)

add_test(NAME adios2-gray-scott-test-run
  COMMAND
    ${MPIEXEC_EXECUTABLE} -np 4
      ${PROJECT_BINARY_DIR}/gray-scott/build/gray-scott
        ${PROJECT_SOURCE_DIR}/gray-scott/testing/settings.json
)
set_tests_properties(adios2-gray-scott-test-run PROPERTIES
  FIXTURES_SETUP gray-scott-run
)

add_test(NAME adios2-gray-scott-test-dump
  COMMAND ./dump.sh
)
set_tests_properties(adios2-gray-scott-test-dump PROPERTIES
  FIXTURES_REQUIRED gray-scott-run
  FIXTURES_SETUP gray-scott-dump
)

#add_test(NAME adios2-gray-scott-test-sha512
#  COMMAND sha512sum -c ${CMAKE_CURRENT_SOURCE_DIR}/gs.bp.dump.sha512
#)
#set_tests_properties(adios2-gray-scott-test-sha512 PROPERTIES
#  FIXTURES_REQUIRED gray-scott-dump
#)
