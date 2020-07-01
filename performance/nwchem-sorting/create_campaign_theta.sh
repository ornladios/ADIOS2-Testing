#! /bin/bash

export PYTHONPATH=$PYTHONPATH:$PWD
directory=$ADIOS_DIR/adios_iotest_nwchem_copro
touch $directory
rm -rf $directory
cheetah create-campaign -e campaign_theta.py -m theta -o $directory -a $PWD

