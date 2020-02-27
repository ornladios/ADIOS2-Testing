#!/bin/bash

if [ $# -ne 4 ]
then
  echo "Usage: $0 setup nprocs1 nprocs2 nprocs3"
  echo "Setups: xg xgn xcg"
  exit 1
fi

SETUP=$1
N1=$2
N2=$3
N3=$4
IOTEST=~/work/ADIOS2/build/bin/adios_iotest

if [ "$SETUP" == "xg" ]; then
    CFG=effis-coupling-xg.txt 
    XML=effis-coupling-xg.xml 
    APP1=XGC
    APP2=GENE
    APP3=
elif [ "$SETUP" == "xgn" ]; then
    CFG=effis-coupling-xgn.txt 
    XML=effis-coupling-xg.xml 
    APP1=XGC
    APP2=GENE
    APP3=NULL
elif [ "$SETUP" == "xcg" ]; then
    CFG=effis-coupling-xcg.txt 
    XML=effis-coupling-xcg.xml 
    APP1=XGC
    APP2=COUPLER
    APP3=GENE
else 
    echo "Invalid setup given. Available setups: xg  xgn  xcg"
    exit  1
fi

printf "Run EFFIS coupling\n"
printf "Exe:  \t $IOTEST\n"
printf "Setup:\t $SETUP\n"
printf "$APP1:\t $N1 processes\n"
printf "$APP2:\t $N2 processes\n"
if [ "x$APP3" != "x" ]; then
    printf "$APP3:\t $N3 processes\n"
fi

rm -rf write_perf_*.txt read_perf_*.txt
rm -rf *_to_*.bp


echo mpirun -n $N1 $IOTEST  -a 1 -c $CFG -x $XML -s -t -d $N1 1 1 : -n $N2 $IOTEST  -a 2 -c $CFG -x $XML -s -t -d $N2 1 1 : -n $N3 $IOTEST  -a 3 -c $CFG -x $XML -s -t -d $N3 1 1
mpirun -n $N1 $IOTEST  -a 1 -c $CFG -x $XML -s -t -d $N1 1 1 : \
       -n $N2 $IOTEST  -a 2 -c $CFG -x $XML -s -t -d $N2 1 1 : \
       -n $N3 $IOTEST  -a 3 -c $CFG -x $XML -s -t -d $N3 1 1

