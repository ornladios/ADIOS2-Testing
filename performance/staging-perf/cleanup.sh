#!/bin/bash

# Run bpls on all ADIOS output files
bpls -lva *.bp &> bpls.out

# Lets remove all large bp files
rm -rf *.bp

