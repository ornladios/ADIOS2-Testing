#! /bin/bash

export PYTHONPATH=$PYTHONPATH:$PWD
directory=$PROJWORK/csc143/xin/adios_iotest_nwchem_copro
touch $directory
rm -rf $directory
cheetah create-campaign -e campaign.py -m rhea -o $directory -a $PWD

