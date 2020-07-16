#!/bin/bash
#
# Usage: setup.sh  INSTALL_DIR   HOSTNAME
# Supported host names: see directories in host-files/
#   Automatically discovered names: summit rhea
#

_PREFIX="*** "

#
# Process args, results in BASE, INSTALL_DIR, HOST
#
BASE=`dirname $0`
cd $BASE
BASE=$PWD
cd -
echo "${_PREFIX}BASE = $BASE"

if [ -z $1 ]; then
    INSTALL_DIR=$PWD
else
    INSTALL_DIR=$1
fi
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR
INSTALL_DIR=$PWD
cd -
echo "${_PREFIX}INSTALL_DIR = $INSTALL_DIR"

if [ -z $2 ]; then
    H=`hostname`
    if [ ${H:0:4} == "rhea" ]; then
        HOST=rhea
    elif [ ${H:0:5} == "login" ]; then
        HOST=summit
    else
        echo "${_PREFIX}ERROR: Cannot determine host name"
        exit 1
    fi
else
    HOST=$2
fi

echo "${_PREFIX}Setup ADIOS2 test suite for host $HOST"
echo "${_PREFIX}                        into directrory $INSTALL_DIR"

#
# Source host specific environment (compilers, modules)
#
source ${BASE}/host-files/${HOST}/modules.sh
echo "${_PREFIX}Setup ADIOS2 test suite for compiler ${COMPILER}"

cd ${INSTALL_DIR}

#
# Clone SPACK
#
if [ ! -d ${INSTALL_DIR}/spack ]; then
    echo "${_PREFIX}Clone spack in ${INSTALL_DIR}/spack"
    git clone -b releases/v0.15 https://github.com/spack/spack.git 
fi

echo "${_PREFIX}Source ${INSTALL_DIR}/spack/share/spack/setup-env.sh"
source ${INSTALL_DIR}/spack/share/spack/setup-env.sh

#
# SPACK host-specific prebuilt packages
#
if [ -x ${BASE}/host-files/${HOST}/setup-packages.sh ]; then
    echo "${_PREFIX}Prepare host specific package descriptions"
    COMPILER=$COMPILER ${BASE}/host-files/${HOST}/setup-packages.sh
fi
if [ -f ${BASE}/host-files/${HOST}/packages.yaml ]; then
    echo "${_PREFIX}Copy host specific package descriptions to Spack"
    cp ${BASE}/host-files/${HOST}/packages.yaml ${INSTALL_DIR}/spack/etc/spack
fi
if [ -f ${BASE}/host-files/${HOST}/config.yaml ]; then
    echo "${_PREFIX}Copy host specific config descriptions to Spack"
    cp ${BASE}/host-files/${HOST}/config.yaml ${INSTALL_DIR}/spack/etc/spack
fi

#
# SPACK compiler setup
#
echo "${_PREFIX}Setup compilers spack..."
spack compiler add --scope site

#
# Build required packages: adios2, codar-cheetah tau
#

echo "${_PREFIX}Looking for package ADIOS2..."
spack find adios2 2>&1 > /dev/null
EX=$?
if [ "$EX" -ne "0" ]; then
    echo "${_PREFIX}Build package ADIOS2 with HDF5"
    spack install adios2@master+hdf5
else
    echo "${_PREFIX}ADIOS2 already built"
fi

echo "${_PREFIX}Looking for package CODAR Cheetah..."
spack find codar-cheetah 2>&1 > /dev/null
EX=$?
if [ "$EX" -ne "0" ]; then
    echo "${_PREFIX}Build package CODAR Cheetah"
    spack install codar-cheetah@develop
else
    echo "${_PREFIX}CODAR Cheetah already built"
fi

echo "${_PREFIX}Looking for package TAU..."
spack find tau 2>&1 > /dev/null
EX=$?
if [ "$EX" -ne "0" ]; then
    echo "${_PREFIX}Build package TAU"
    spack install tau+mpi
else
    echo "${_PREFIX}TAU already built"
fi



#
# Create setup-env.sh for users to source
#
# Replace / with \/ in paths
INSTALL_DIR_SED=${INSTALL_DIR//\//\\\/}
BASE_DIR_SED=${BASE//\//\\\/}
echo "${_PREFIX}Prepare setup-env.sh script for users"
cat ${BASE}/setup-env.sh.in | \
    sed -e "s/#INSTALL_DIR#/${INSTALL_DIR_SED}/g" \
        -e "s/#BASE_DIR#/${BASE_DIR_SED}/g" \
        -e "s/#HOST#/${HOST}/g" \
    > ${INSTALL_DIR}/setup-env.sh

#
# Create modules.sh for setup-env.sh to source
#
cp ${BASE}/host-files/${HOST}/modules.sh ${INSTALL_DIR}/modules-$HOST.sh


