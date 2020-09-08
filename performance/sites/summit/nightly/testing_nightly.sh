#!/bin/bash

set -e
set +x

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

if [ -d ${WORK_DIR}/performance ]
then
  echo "Cleaning up existing worktree in ${WORK_DIR}/performance"
  rm -rf ${WORK_DIR}/performance
fi
mkdir -p ${WORK_DIR}/performance
git clone https://github.com/ornladios/adios2-testing.git ${WORK_DIR}/performance/source

mkdir -p ${WORK_DIR}/performance/build
cd ${WORK_DIR}/performance/build
cmake \
  -DSITE=summit -DBUILDNAME=adios2-nightly \
  -DMACHINE=summit -DSWEEP_GROUP=small \
  -DENV_SETUP=${WORK_DIR}/env_run.sh \
  -DTEST_OUTPUT_BASE_DIR=${WORK_DIR}/performance/run \
  ${WORK_DIR}/performance/source/performance

make VERBOSE=1 Nightly
