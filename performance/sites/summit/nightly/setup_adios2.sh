#!/bin/bash

set -e

if [ -z "${SCRIPT_DIR}" ]
then
  echo "Error: ENV{SCRIPT_DIR} is not defined"
  exit 1
elif [ -z "${WORK_DIR}" ]
then
  echo "Error: ENV{WORK_DIR} is not defined"
  exit 2
fi

source ${SCRIPT_DIR}/env_build.sh

if [ -d ${WORK_DIR}/adios2 ]
then
  echo "Cleaning up existing build in ${WORK_DIR}/adios2"
  rm -rf ${WORK_DIR}/adios2
fi
mkdir -p ${WORK_DIR}/adios2/
git clone https://github.com/ornladios/adios2.git ${WORK_DIR}/adios2/source

mkdir -p ${WORK_DIR}/adios2/build
cd ${WORK_DIR}/adios2/build
cmake \
  -DCMAKE_INSTALL_PREFIX=${WORK_DIR}/adios2/install \
  -DBUILD_TESTING=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DADIOS2_BUILD_EXAMPLES=OFF \
  ../source
make -j8 install
