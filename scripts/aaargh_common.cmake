# Client maintainer: chuck.atkins@kitware.com
set(CTEST_SITE "aaargh.kitware.com")
set(CTEST_BUILD_CONFIGURATION Release)
set(CTEST_CMAKE_GENERATOR "Unix Makefiles")
set(CTEST_BUILD_FLAGS "-k -j72")
set(CTEST_TEST_ARGS PARALLEL_LEVEL 1)

set(dashboard_model Experimental)
set(CTEST_DASHBOARD_ROOT ${CMAKE_CURRENT_BINARY_DIR}/${CTEST_BUILD_NAME})

find_package(EnvModules REQUIRED)
env_module(purge)
env_module(load gnu8)
env_module(load openmpi3)
env_module(load phdf5)
env_module(load netcdf)
env_module(load netcdf-fortran)
env_module(load pnetcdf)
env_module(load py2-numpy)
env_module(load py2-mpi4py)

set(ENV{CC}  gcc)
set(ENV{CXX} g++)
set(ENV{FC}  gfortran)

include(${CMAKE_CURRENT_LIST_DIR}/adios2_external-testing_common.cmake)
