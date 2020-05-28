# Synthetic staging-performance-tests

## To run Cheetah:

cheetah create-campaign -a \<path-to-exe-and-input-files\> -e \<path to spec file\> -m summit -o \<where to create campaign on gpfs\>

Once the campaign is created, you will see path-to-campaign/your-username/ . Either run `run-all.sh` here to launch all jobs, or cd into one of the directories and launch `submit.sh`.


## Monitoring a campaign:

cheetah status \<campaign path\> options
-n for summary

## Generate a performance report:

cheetah generate-report \<campaign path\>

## Execution Plan

10 jobs of different sized with 30 cases:

adios_iotest runs with modes (5):
   BP4   - write and read one after the other
   SST/TCP
   SST/RDMA
   SSC       - MPMD mode reguired, use -f <appfile> option for jsrun
   InSituMPI - MPMD mode required, use -f <appfile> option for jsrun

Input setup (6):
  2x1: 1/2 readers
  8x1: 1/8 readers

  1MB per process
  16MB
  512MB

Co-location (2):
  Co-located - each 2 or 8 writer has 1 reader on the same node
  Separated - readers are on separate nodes from writers

Nodes (5):
  co-location: 8 (test), 512, 1024, 2048, 4096
  separate:    8+4,  512+256, 1024+512, 2048+1024,

Processes:
  co-location:  32 writer + 16 or 4 readers per node
  separate:     32 writer per node, 32 readers per node
  8 nodes:
     co-location:  256 writers    128/32 readers
     separate:     256 writers    128/32 readers
  512 nodes:
     co-location:  16384 writers  8192/2048 readers
     separate:     16384 writers  8192/2048 readers
  1024 nodes:
     co-location:  32768 writers  16384/4096 readers
     separate:     32768 writers  16384/4096 readers
  2048 nodes:
     co-location:  65536 writers  32768/8192 readers
     separate:     65536 writers  32768/8192 readers
  4096 nodes:
     co-location:  131072 writers  65536/16384 readers

