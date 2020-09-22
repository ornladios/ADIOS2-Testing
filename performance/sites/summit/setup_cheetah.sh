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

if [ -d ${WORK_DIR}/cheetah ]
then
  echo "Cleaning up existing clone in ${WORK_DIR}/cheetah"
  rm -rf ${WORK_DIR}/cheetah
fi
mkdir -p ${WORK_DIR}
git clone https://github.com/CODARcode/cheetah.git ${WORK_DIR}/cheetah
