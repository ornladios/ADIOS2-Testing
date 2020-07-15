# Performance test suite: tests

## Summit

$ cd /ccs/proj/csc303
$ . ./adios2-test-suite/summit/setup-env.sh 
Note: this will  spack load adios2 tau codar-cheetah
$ cd ADIOS2-Testing/performance/staging-perf/
$ ln -s `which adios2_iotest`
$ export PYTHONPATH=$PWD:$PYTHONPATH
$ rm -rf  $PROJWORK/csc303/$USER/suite/staging-perf
$ cheetah create-campaign -a . -e campaign.py -m summit -o $PROJWORK/csc303/$USER/suite/staging-perf
$ cd $PROJWORK/csc303/$USER/suite/staging-perf/$USER
$ ./run-all.sh

