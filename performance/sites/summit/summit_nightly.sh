#!/bin/bash

set -e

export SCRIPT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
echo ${SCRIPT_DIR}/dashboard.sh "9:00pm" summit small experimental summit-xgc-restart-small | at -M now
