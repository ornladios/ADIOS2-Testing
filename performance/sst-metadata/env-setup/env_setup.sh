module load gcc/6.4.0
module load python
module load cmake

alias gcc='/sw/summit/gcc/6.4.0/bin/gcc'
alias g++='/sw/summit/gcc/6.4.0/bin/g++'
alias gfortran='/sw/summit/gcc/6.4.0/bin/gfortran'
export CC=/sw/summit/gcc/6.4.0/bin/gcc
export CXX=/sw/summit/gcc/6.4.0/bin/g++
export FC=/sw/summit/gcc/6.4.0/bin/gfortran

export PYTHONPATH=$PYTHONPATH:/gpfs/alpine/world-shared/csc299/sw/cheetah
export PATH=$PATH:/gpfs/alpine/world-shared/csc299/sw/cheetah/bin

export libpath=/gpfs/alpine/csc303/proj-shared/jason/lib

export PATH=$libpath/bin:$PATH
export CPATH=$libpath/include:$CPATH
export LIBRARY_PATH=$libpath/lib:$libpath/lib64:$LIBRARY_PATH
export LD_LIBRARY_PATH=$libpath/lib:$libpath/lib64:$LD_LIBRARY_PATH
