configure_file(adios2.xml adios2.xml COPYONLY)
configure_file(dump.sh.in dump.sh @ONLY)

add_test(NAME adios2-heat2d-test-run
  COMMAND
    ${MPIEXEC_EXECUTABLE} -np 4
      ${PROJECT_BINARY_DIR}/heat2d/source/Tutorial/heat2d/fortran/simulation/heatSimulation_adios2
        heat.bp 2 2 256 256 6 500
)
set_tests_properties(adios2-heat2d-test-run PROPERTIES
  FIXTURES_SETUP heat2d-run
)

add_test(NAME adios2-heat2d-test-dump
  COMMAND ./dump.sh
)
set_tests_properties(adios2-heat2d-test-dump PROPERTIES
  FIXTURES_REQUIRED heat2d-run
  FIXTURES_SETUP heat2d-dump
)

add_test(NAME adios2-heat2d-test-check
  COMMAND ${CMAKE_COMMAND}
    -E compare_files
    ${CMAKE_CURRENT_SOURCE_DIR}/heat.bp.dump
    ${CMAKE_CURRENT_BINARY_DIR}/heat.bp.dump
)
set_tests_properties(adios2-heat2d-test-check PROPERTIES
  FIXTURES_REQUIRED heat2d-dump
)
