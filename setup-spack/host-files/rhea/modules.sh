
module unload gcc pgi intel
module unload python

module load gcc/8.4.0
module load cmake
module load python/3.7.0-anaconda3-2018.12
module load rdma-core



GCCVERSION=`module list 2>&1 | grep gcc | sed -e "s/^.*gcc\///" | sed -e "s/ .*//"`
COMPILER=gcc@${GCCVERSION}

