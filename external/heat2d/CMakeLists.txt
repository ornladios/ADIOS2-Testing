set_directory_properties(PROPERTIES EP_BASE ${CMAKE_CURRENT_BINARY_DIR})

ExternalProject_Add(heat2d
  DEPENDS ${ADIOS2_DEP}
  GIT_REPOSITORY https://github.com/chuckatkins/adiosvm.git
  GIT_TAG remove-override
  GIT_SHALLOW ON
  BUILD_IN_SOURCE TRUE
  PREFIX .
  DOWNLOAD_DIR download
  STAMP_DIR stamp
  SOURCE_DIR source
  INSTALL_DIR install
  CONFIGURE_COMMAND ""
  BUILD_COMMAND
    $(MAKE) -C Tutorial/heat2d/fortran ADIOS2_DIR=${ADIOS2_ROOT} adios2
  INSTALL_COMMAND ""
)

add_subdirectory(testing)
