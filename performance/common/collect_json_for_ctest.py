#!/usr/bin/env python3
import json
import sys
import os
import glob
from collections import defaultdict
from statistics import *

print_measurement = lambda k, v: print('<DartMeasurement type="numeric/double" name="%s">%f</DartMeasurement>' % (k, v))

def collect_stats(group_dir):
    all_data = defaultdict(list)
    inputs = sorted(glob.glob(group_dir+'/*/cheetah_user_report.json'))
    for fname in inputs:
        with open(fname) as f:
            run = os.path.basename(os.path.dirname(fname))
            print('Procesing %s' % run)
            raw_data = json.load(f)
            valid_data = {}
            skip = False
            for k, v in raw_data.items():
                try:
                    valid_data[k] = float(v)
                except ValueError:
                    skip = True
            if skip:
                print('Skipping due to invalid numeric value(s) for one or more measurements')
                continue

            for k, v in valid_data.items():
                all_data[k].append(v)

    for key, values in all_data.items():
        print_measurement(key+"_min", min(values))
        print_measurement(key+"_max", max(values))
        print_measurement(key+"_mean", mean(values))
        if len(values) > 1:
            print_measurement(key+"_stdev", stdev(values))

if __name__ == "__main__":
    collect_stats(sys.argv[1])
