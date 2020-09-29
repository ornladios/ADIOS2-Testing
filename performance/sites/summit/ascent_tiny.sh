#!/bin/bash

set -e

export SCRIPT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
echo ${SCRIPT_DIR}/dashboard.sh "9:00pm" summit tiny experimental ascent-xgc-restart-tiny | at -M now
