#!/usr/bin/env python3
import json


#----------------------------------------------------------------------------#
def get_total_time(stdout_file):
    """
    Open stdout and read the line 'ADIOS IOTEST test time'
    to get the total runtime of the application
    """

    lines = []
    total_time = 'N/A'

    # Open stdout file and read all lines into a list
    try:
        with open(stdout_file) as f:
             lines = f.readlines()
    except:
        print("Warn: Could not find {}".format(stdout_file))
           
    # Parse lines to get the total runtime
    for line in lines:
        if 'ADIOS IOTEST test time' in line:
            try:
                total_time = line.split('ADIOS IOTEST test time ')[1].split('seconds')[0].strip()
            except:
                print("Warn: Could not parse line about total time. Skipping..")

    # Return the total runtime obtained from the stdout
    return total_time
#----------------------------------------------------------------------------#


d = {}
d['writer_time_stdout'] = get_total_time('codar.workflow.stdout.writer')
d['reader_time_stdout'] = get_total_time('codar.workflow.stdout.reader')

# Write data to 'cheetah_user_report.json'
try:
    with open("cheetah_user_report.json", "w") as f:
        json.dump(d,f)
except:
    print("Warn: Could not write times from stdout to cheetah_user_report.json.")

