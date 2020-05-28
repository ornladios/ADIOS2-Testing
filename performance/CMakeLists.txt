cmake_minimum_required(VERSION 3.12)

project(adios2-performance-testing C CXX Fortran)

include(ExternalProject)
include(CTest)
set(BUILD_TESTING ON CACHE BOOL "" FORCE)
mark_as_advanced(BUILD_TESTING)
enable_testing()

include(ProcessorCount)
ProcessorCount(NCPUS)
set(ADIOS2_PARALLEL_BUILD_LEVEL ${NCPUS} CACHE STRING
  "Parallel build level of dependencies"
)

find_package(MPI REQUIRED)

add_subdirectory(adios2)

add_subdirectory(e3sm-mmf)
