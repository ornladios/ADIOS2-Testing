#!/bin/bash

# Run bpls on all ADIOS output files
touch bpls.out
for bp_file in *.bp; do
    echo -e "\n#---------------- bpls -lva $bp_file ----------------#\n" &>> bpls.out
    bpls -lva "$bp_file" &>> bpls.out
done

# Lets remove all large bp files
# rm -rf *.bp


