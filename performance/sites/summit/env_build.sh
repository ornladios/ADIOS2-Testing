module purge
module load git
module load cmake
module load xl
module load python/3.7.0
module load bzip2
module load zlib
module load libpng
module load zeromq
module load spectrum-mpi
module load hdf5
module load libfabric
module load rdma-core
export LD_PRELOAD="/usr/lib64/libibverbs.so.1:/usr/lib64/librdmacm.so.1"
