#!/bin/bash

set -e

export SCRIPT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

# Update ourselves and re-run
cd "${SCRIPT_DIR}"
module purge
module load git
git log --pretty=format:"%h %aI [%an] %s" | head -1
if [ "${SKIP_UPDATE}" != "1" ]
then
  cd "${SCRIPT_DIR}"
  if git pull --ff-only
  then
    git submodule update --init --recursive
  fi
  export SKIP_UPDATE=1
  exec "${BASH_SOURCE}"
  exit $?
fi

# Substitute for cron
at -M -f "${BASH_SOURCE}" 9:00 PM tomorrow 

export TAG=$(date +%Y%m%d)
export PERF_SOURCE_DIR=$(readlink -f ${SCRIPT_DIR}/../../..)
export WORK_DIR=${PROJWORK}/csc303/summit/nightly/adios2-testing/${TAG}

mkdir -p ${WORK_DIR}
sed -e "s|SCRIPT_DIR|${SCRIPT_DIR}|" -e "s|WORK_DIR|${WORK_DIR}|" ${SCRIPT_DIR}/env_run.sh.in > ${WORK_DIR}/env_run.sh

${SCRIPT_DIR}/setup_adios2.sh
${SCRIPT_DIR}/setup_cheetah.sh
${SCRIPT_DIR}/testing_nightly.sh
