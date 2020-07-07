#!/bin/bash

APP1_N=$(awk '/app1/,/}/ {if ($0 ~ /nprocs/) print $NF}' codar.cheetah.run-params.json | sed 's/[,\"]//g')
APP1_X=1
while [ $((APP1_X * APP1_X * APP1_X)) -lt $APP1_N ] ; do
    APP1_X=$((APP1_X + 1))
done
APP2_N=$(awk '/app2/,/}/ {if ($0 ~ /nprocs/) print $NF}' codar.cheetah.run-params.json | sed 's/[,\"]//g')
READ_PATTERN=$(awk '/read pattern/ { print $NF }' codar.cheetah.run-params.json | sed 's/[,\"]//g')
if [ "${READ_PATTERN}" == "chunk" ] ; then
    APP2_X=1
    while [ $((APP2_X * APP2_X * APP2_X)) -lt $APP2_N ] ; do
        APP2_X=$((APP2_X + 1))
    done
    CHUNK2_LEN=$((CUBE_LEN / APP2_X))
fi
CUBE_LEN=$(awk '/cube length/ { print $NF }' codar.cheetah.run-params.json | sed 's/[,\"]//g')

CHUNK_LEN=$((CUBE_LEN / APP1_X))
READ_PATTERN=$(awk '/read pattern/ { print $NF }' codar.cheetah.run-params.json | sed 's/[,\"]//g')

echo "group  io_T1" > planar_reads.txt
echo "
  array   double  a           3    ${CHUNK_LEN}   ${CHUNK_LEN}   ${CHUNK_LEN}     X       Y   Z
" >> planar_reads.txt

case $READ_PATTERN in

ij)
    echo "
group  io_T2_in
  array   double  a           3    ${CUBE_LEN}   ${CUBE_LEN} 1       1 1 XYZ"  >> planar_reads.txt
    ;;
ik)
   echo "
group  io_T2_in
  array   double  a           3    ${CUBE_LEN} 1  ${CUBE_LEN}        1 XYZ 1"  >> planar_reads.txt
    ;;
jk)
  echo "
group  io_T2_in
  array   double  a           3    1 ${CUBE_LEN}  ${CUBE_LEN}        XYZ 1 1"  >> planar_reads.txt
    ;;
chunk)
   echo "
group  io_T2_in
  array   double  a           3    ${CHUNK2_LEN}   ${CHUNK2_LEN}   ${CHUNK2_LEN}     X       Y   Z"  >> planar_reads.txt
    ;;
esac

echo "app 1
  steps   3
  sleep   5.0      
  write   stream_T1.bp    io_T1

app 2
  steps   3
  read  next  stream_T1.bp    io_T2_in  -1 
  sleep   2.0"  >> planar_reads.txt
