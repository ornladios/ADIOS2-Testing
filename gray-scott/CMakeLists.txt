set_directory_properties(PROPERTIES EP_BASE ${CMAKE_CURRENT_BINARY_DIR})

ExternalProject_Add(gray-scott
  DEPENDS ${ADIOS2_DEP}
  GIT_REPOSITORY https://github.com/pnorbert/adiosvm.git
  GIT_TAG master
  GIT_SHALLOW ON
  SOURCE_SUBDIR Tutorial/gray-scott
  PREFIX .
  DOWNLOAD_DIR download
  STAMP_DIR stamp
  SOURCE_DIR source
  BINARY_DIR build
  INSTALL_DIR install
  CMAKE_ARGS
    -DCMAKE_POLICY_DEFAULT_CMP0074=NEW
    -DADIOS2_ROOT=${ADIOS2_ROOT}
  INSTALL_COMMAND ""
)

add_subdirectory(testing)
