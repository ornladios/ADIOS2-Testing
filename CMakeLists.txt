cmake_minimum_required(VERSION 3.12)

project(adios2-external-testing C CXX Fortran)

include(ExternalProject)
include(CTest)
set(BUILD_TESTING ON CACHE BOOL "" FORCE)
enable_testing()

find_package(MPI REQUIRED)

if(ADIOS2_INTERNAL OR NOT ADIOS2_ROOT)
  add_subdirectory(adios2)
  set(ADIOS2_DEP adios2)
else()
  find_package(ADIOS2 REQUIRED)
  set(ADIOS2_DEP adios2::adios2)
endif()

option(ADIOS2_EXTERNAL_TESTING_HEAT2D "Build the Heat Transfer MiniApp" OFF)
if(ADIOS2_EXTERNAL_TESTING_HEAT2D)
  add_subdirectory(heat2d)
endif()

option(ADIOS2_EXTERNAL_TESTING_GRAYSCOTT "Build the Gray-Scott MiniApp" OFF)
if(ADIOS2_EXTERNAL_TESTING_GRAYSCOTT)
  add_subdirectory(gray-scott)
endif()

option(ADIOS2_EXTERNAL_TESTING_LAMMPS "Build LAMMPS" OFF)
if(ADIOS2_EXTERNAL_TESTING_LAMMPS)
  add_subdirectory(lammps)
endif()

option(ADIOS2_EXTERNAL_TESTING_PIO "Build ParallelIO" OFF)
if(ADIOS2_EXTERNAL_TESTING_PIO)
  add_subdirectory(pio)
endif()
