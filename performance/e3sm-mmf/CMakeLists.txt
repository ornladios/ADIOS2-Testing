set(ADIOS2_IOTEST "${ADIOS2_ROOT}/bin/adios_iotest")

configure_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/iotest_wrapper.sh.in
  ${CMAKE_CURRENT_BINARY_DIR}/iotest_wrapper.sh
  @ONLY
)

set(ADIOS2_IOTEST_M ${MPIEXEC_MAX_NUMPROCS} CACHE STRING "")
set(ADIOS2_IOTEST_N 1 CACHE STRING "")

add_test(NAME E3SM-IOTest-Write
  COMMAND bash ${CMAKE_CURRENT_BINARY_DIR}/iotest_wrapper.sh
    ${CMAKE_CURRENT_SOURCE_DIR}/IOTest1-config.xml
    ${CMAKE_CURRENT_SOURCE_DIR}/IOTest1-config.txt
    1 ${ADIOS2_IOTEST_M} ${ADIOS2_IOTEST_N}
)
add_test(NAME E3SM-IOTest-Read
  COMMAND bash ${CMAKE_CURRENT_BINARY_DIR}/iotest_wrapper.sh
    ${CMAKE_CURRENT_SOURCE_DIR}/E3SM-IOTest-config.xml
    ${CMAKE_CURRENT_SOURCE_DIR}/E3SM-IOTest-config.txt
    2 ${ADIOS2_IOTEST_M} ${ADIOS2_IOTEST_N}
)
set_tests_properties(E3SM-IOTest-Write PROPERTIES FIXTURES_SETUP    E3SM-IOTest)
set_tests_properties(E3SM-IOTest-Read  PROPERTIES FIXTURES_REQUIRED E3SM-IOTest)
