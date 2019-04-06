set_directory_properties(PROPERTIES EP_BASE ${CMAKE_CURRENT_BINARY_DIR})

ExternalProject_Add(lammps
  DEPENDS ${ADIOS2_DEP}
  GIT_REPOSITORY https://github.com/ornladios/lammps.git
  GIT_TAG adios2-external-testing
  GIT_SHALLOW ON
  SOURCE_SUBDIR cmake
  PREFIX .
  DOWNLOAD_DIR download
  STAMP_DIR stamp
  SOURCE_DIR source
  BINARY_DIR build
  INSTALL_DIR install
  CMAKE_ARGS
    -DCMAKE_POLICY_DEFAULT_CMP0074=NEW
    -DADIOS2_ROOT=${ADIOS2_ROOT}
    -DBUILD_MPI=yes
    -DBUILD_EXE=yes
    -DBUILD_LIB=no
    -DBUILD_DOC=no
    -DLAMMPS_SIZES=smallbig
    -DPKG_USER-ADIOS=yes
  INSTALL_COMMAND ""
)

add_subdirectory(testing)
