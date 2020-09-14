# Performance test suite: tests

## Summit

$ cd /ccs/proj/csc303
$ ./ADIOS2-Testing/setup-spack/setup.sh adios2-test-suite/summit
$ . ./adios2-test-suite/summit/setup-env.sh 
$ spack find -dp adios2 
$ spack find -dp codar-cheetah
$ spack find -dp tau

## Rhea

$ cd /ccs/proj/csc303
$ ./ADIOS2-Testing/setup-spack/setup.sh adios2-test-suite/rhea
$ . ./adios2-test-suite/rhea/setup-env.sh 
$ spack find -dp adios2 
$ spack find -dp codar-cheetah
$ spack find -dp tau

## Local machine

$ cd $HOME/suite
$ git clone https://github.com/ornladios/ADIOS2-Testing
$ ./ADIOS2-Testing/setup-spack/setup.sh adios2-test-suite
$ . ./adios2-test-suite/setup-env.sh 
$ spack find -dp adios2 
$ spack find -dp codar-cheetah
$ spack find -dp tau

