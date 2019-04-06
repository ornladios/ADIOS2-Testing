configure_file(adios2_config.xml adios2_config.xml COPYONLY)
configure_file(check_results.sh.in check_results.sh)

add_test(NAME adios2-lammps-test-run
  COMMAND
    ${MPIEXEC_EXECUTABLE} -np 4
      ${PROJECT_BINARY_DIR}/lammps/build/lmp
        -in ${CMAKE_CURRENT_SOURCE_DIR}/in.test
)
set_tests_properties(adios2-lammps-test-run PROPERTIES
  FIXTURES_SETUP lammps
)

add_test(NAME adios2-lammps-test-check
  COMMAND ./check_results.sh
)
set_tests_properties(adios2-lammps-test-check PROPERTIES
  FIXTURES_REQUIRED lammps
)
