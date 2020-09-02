#!/bin/bash

if [ $# -lt 2 ]
then
  echo "Usage: $0 /path/to/env.sh execname arg1 ... argn"
  exit 1
fi

source "$1"
shift

exec "$@"
