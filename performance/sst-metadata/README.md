# Synthetic SST writer-side metadata aggregation comparisons.   SST metadata
  aggregation idffers between FFS and BP Marshalling principally in that BP
  metadata aggregation performs its own MPI operations to aggregate, in
  addition to the calls that SST must use for it's on synchronization
  purposes.  This campaign aims to test the impact of that difference by
  comparing writer-side data generation and marshalling *ONLY*.  That is,
  data is not transmitted and we use ReaderRendezvousCount = 0 to ensure
  that the writer doesn't wait for any readers.

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

adios_iotest runs with modes (2):
   SST-ffs
   SST-bp

Input setup (6):
   many-vars iotest input file has 200 variables in it, each small 3d arrays (2x2x2)


Nodes (9):
  2, 4, 8, 32, 64, 128, 512, 2048, 8192

Processes:
  32 writer per node


