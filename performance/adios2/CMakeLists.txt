set(ADIOS2_CACHE_SCRIPT "" CACHE FILEPATH
  "A CMake cache script to use when building ADIOS."
)
set(adios2_cache_opt)
if(ADIOS2_CACHE_SCRIPT)
  set(adios2_cache_opt "-C${ADIOS2_CACHE_SCRIPT}")
endif()

set_directory_properties(PROPERTIES EP_BASE ${CMAKE_CURRENT_BINARY_DIR})
set(ADIOS2_ROOT ${CMAKE_CURRENT_BINARY_DIR}/build CACHE INTERNAL "")
ExternalProject_Add(adios2
  GIT_REPOSITORY https://github.com/ornladios/adios2.git
  GIT_TAG master
  GIT_SHALLOW ON
  PREFIX .
  DOWNLOAD_DIR download
  STAMP_DIR stamp
  SOURCE_DIR source
  BINARY_DIR build
  CMAKE_ARGS
    ${adios2_cache_opt}
    -DADIOS2_BUILD_TESTING=OFF
    -DADIOS2_BUILD_EXAMPLES=OFF
  BUILD_COMMAND
    ${CMAKE_COMMAND} --build <BINARY_DIR> -j ${ADIOS2_PARALLEL_BUILD_LEVEL}
  INSTALL_COMMAND ""
)
