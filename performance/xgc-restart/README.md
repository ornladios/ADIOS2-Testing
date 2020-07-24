# Synthetic xgc-restart test

## To run Cheetah:

Add the current directory to PYTHONPATH `export PYTHONPATH=$PWD:$PYTHONPATH`, so that Cheetah finds the current py files when it creates the campaign.

cheetah create-campaign -a \<path-to-exe-and-input-files\> -e \<path to spec file\> -m summit -o \<where to create campaign on gpfs\>

Once the campaign is created, you will see path-to-campaign/your-username/ . Either run `run-all.sh` here to launch all jobs, or cd into one of the directories and launch `submit.sh`.


## Monitoring a campaign:

cheetah status \<campaign path\> options
-n for summary

## Generate a performance report:

cheetah generate-report \<campaign path\>

## Execution Plan

