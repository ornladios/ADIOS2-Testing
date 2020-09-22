#!/bin/bash

set -e

function usage()
{
  echo "Usage: $0 [nexttime [machinename [sweepgroup [dashboardtype [buildname]]]]]"
  echo "  nexttime       When to schedule he next run (now + tomorrow)"
  echo "  machinename    The machine name passed to cheetah $(hostname -s)"
  echo "  sweepgroup     The Cheetah sweep group to use (<empty>)"
  echo "  dashboardtype  The CDash model to use when uploading (Experimental)"
  echo "  buildname      The CDash build name (<machine>-adios2-testing-<sweepgroup>)"
}

if [ $# -gt 5 ]
then
  usage
  exit 1
fi

if [ "$1" == "-h" -o "$1" == "--help" ]
then
  usage
  exit 1
fi

export SCRIPT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
THIS_SCRIPT=$(readlink -f ${BASH_SOURCE})

# Update ourselves and re-run
cd "${SCRIPT_DIR}"
module purge
module load git
git log --pretty=format:"%h %aI [%an] %s" | head -1
if [ "${SKIP_UPDATE}" != "1" ]
then
  echo
  echo
  echo "Updating self..."
  echo
  echo
  cd "${SCRIPT_DIR}"
  if git pull --ff-only
  then
    git submodule update --init --recursive
  fi
  export SKIP_UPDATE=1
  echo
  echo
  echo "Re-running with updated self..."
  echo
  echo
  exec ${THIS_SCRIPT} "$@"
  exit $?
fi

if [ $# -ge 1 ]
then
  NEXTTIME="$1"
  if [ $# -ge 2 ]
  then
    MACHINE="$2"
    if [ $# -ge 3 ]
    then
      SG="$3"
      if [ $# -ge 4 ]
      then
        DT="$4"
        if [ $# -eq 5 ]
        then
          BUILDNAME="$5"
        else
          if [ -z "${SG}" ]
          then
            BUILDNAME="${MACHINE}_adios2-testing"
          else
            BUILDNAME="${MACHINE}_adios2-testing_${SG}"
          fi
        fi
      else
        DT="experimental"
        if [ -z "${SG}" ]
        then
          BUILDNAME="${MACHINE}_adios2-testing"
        else
          BUILDNAME="${MACHINE}_adios2-testing_${SG}"
        fi
      fi
    else
      SG=""
      DT="experimental"
      BUILDNAME="${MACHINE}_adios2-testing"
    fi
  else
    MACHINE=$(hostname -s)
    SG=""
    DT="experimental"
    BUILDNAME="${MACHINE}_adios2-testing"
  fi
else
  NEXTTIME="tomorrow"
  MACHINE=$(hostname -s)
  SG=""
  DT="experimental"
  BUILDNAME="${MACHINE}_adios2-testing"
fi

echo "NEXTTIME   : ${NEXTTIME}"
echo "MACHINE    : ${MACHINE}"
echo "SWEEPGROUP : ${SG}"
echo "DASHBOARD  : ${DT}"
echo "BUILDNAME  : ${BUILDNAME}"
export MACHINE SG DT BUILDNAME

# Substitute for cron
if [ "${SKIP_NEXT}" != "1" ]
then
  echo
  echo
  echo "Scheduling next run for \"${NEXTTIME}\"..."
  echo
  echo
  echo ${THIS_SCRIPT} "$@" | at -M "${NEXTTIME}"
fi

echo
echo
echo "Running the dashboard..."
echo
echo

export TAG=$(date +%Y%m%d-%H%m%S)
export PERF_SOURCE_DIR=$(readlink -f ${SCRIPT_DIR}/../..)
export WORK_DIR=${PROJWORK}/csc303/dashboard/adios2-testing/${BUILDNAME}-${TAG}

mkdir -p ${WORK_DIR}
sed -e "s|SCRIPT_DIR|${SCRIPT_DIR}|" -e "s|WORK_DIR|${WORK_DIR}|" ${SCRIPT_DIR}/env_run.sh.in > ${WORK_DIR}/env_run.sh

${SCRIPT_DIR}/setup_adios2.sh   &>${WORK_DIR}/log.txt
${SCRIPT_DIR}/setup_cheetah.sh  &>>${WORK_DIR}/log.txt
${SCRIPT_DIR}/run_testing.sh    &>>${WORK_DIR}/log.txt
