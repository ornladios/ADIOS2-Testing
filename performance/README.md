# Performance test suite: tests

## Manually running performance tests on Summit

$ cd /ccs/proj/csc303
$ . ./adios2-test-suite/summit/setup-env.sh 
Note: this will  spack load adios2 tau codar-cheetah
$ cd ADIOS2-Testing/performance/staging-perf/
$ ln -s `which adios2_iotest`
$ export PYTHONPATH=.:$PYTHONPATH
$ rm -rf  $PROJWORK/csc303/$USER/suite/staging-perf
$ cheetah create-campaign -a . -e campaign.py -m summit -o $PROJWORK/csc303/$USER/suite/staging-perf
$ cd $PROJWORK/csc303/$USER/suite/staging-perf/$USER
$ ./run-all.sh

## Using CTest to run performance tests and submit them to CDash

While the above describes how to manually generate cheetah campaigns and run performance tests, you can also use the CMake / CTest / CDash infrastructure to run the performance tests in an automated way and submit the results to a public dashboard.  To do so, the following is required in your environment:

* git
* cmake
* python3

The process will also try to look up and use pre-defined test environment setup scripts but the option exists for them to be overridden by the user.

The following options can be specified by the user at configure time:

| VAR | Default | Description |
|-----|---------|-------------|
| SITE | hostname | The site name for the build on CDash |
| BUILDNAME | Linux-unknown | The build name on CDash |
| MACHINE | local | The machine model used by cheetah |
| TEST_OUTPUT_BASE_DIR | <build-dir>/test-output | The working directory used by the cheetah campaigns |
| ENV_SETUP | <empty> | The environment setup script used for running the performance tests |
| ENABLE_XGC_RESTART | TRUE | Enable the xgc-restart performance tests |
| XGC_ENV_SETUP | `xgc-restart/env-setup/env_setup_${MACHINE}.sh` | The environment setup script specific to the xgc-restart tests.  Overrides `ENV_SETUP` if empty.|


The three steps configure, build, and tests, then perform the following actions:
* configure: Generate the cheetah campaign
* build: Submit the test jobs, wait for their completion, generate the cheeta report
* test: Process and summarize the individual cheetah campaign groups and combine the results of each run to be submitted to CDash


### CTest Example 1: Runing the benchmarks interactively

Prep:
```
[atkins3@rhea-login4g ~]$ module purge
[atkins3@rhea-login4g ~]$ module laod git cmake python/3.7.0-anaconda3-2018.12
[atkins3@rhea-login4g ~]$ mkdir adios2-testing
[atkins3@rhea-login4g ~]$ cd adios2-testing/
[atkins3@rhea-login4g adios2-testing]$ git clone https://github.com/ornladios/adios2-testing.git source
Cloning into 'source'...
remote: Enumerating objects: 242, done.
remote: Counting objects: 100% (242/242), done.
remote: Compressing objects: 100% (165/165), done.
remote: Total 738 (delta 111), reused 185 (delta 76), pack-reused 496
Receiving objects: 100% (738/738), 5.44 MiB | 0 bytes/s, done.
Resolving deltas: 100% (348/348), done.
[atkins3@rhea-login4g adios2-testing]$ mkdir build
[atkins3@rhea-login4g adios2-testing]$ cd build
[atkins3@rhea-login4g build]$
```

Configure:
```
[atkins3@rhea-login4g build]$ cmake -DSITE=rhea -DBUILDNAME=adios2-default -DMACHINE=rhea -DTEST_OUTPUT_BASE_DIR=${MEMBERWORK}/csc303/performance-testing/rhea/tmp-test ../source/performance
Using ENV_SETUP="/ccs/home/atkins3/adios2-testing/source/performance/xgc-restart/env-setup/env_setup_rhea.sh"
-- Locating cheetah...
-- Locating cheetah... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/codar-cheetah-develop-zotwnryl3hox2iylnofurbbo6r3e3y6n/bin/cheetah
-- Locating tau_exec...
-- Locating tau_exec... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/tau-2.29-tc3ik7ihp5p5sz6q42gmysr3vcs34xme/bin/tau_exec
-- Locating bpls...
-- Locating bpls... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/adios2-master-qu6mjxrg7vmpom7w7nh5wxixmgrdm22a/bin/bpls
-- Locating adios2_iotest...
-- Locating adios2_iotest... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/adios2-master-qu6mjxrg7vmpom7w7nh5wxixmgrdm22a/bin/adios2_iotest
Generating xgc-restart test scripts in "/gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart"
--   Generating campaing configuration
--   Generating run scripts
--   Generating full cheetah campaign
-- Adding test group: xgc-restart-128-processes-bp4
-- Adding test group: xgc-restart-2048-processes-bp4
-- Adding test group: xgc-restart-512-processes-bp4
-- Configuring done
-- Generating done
-- Build files have been written to: /ccs/home/atkins3/adios2-testing/build
[atkins3@rhea-login4g build]$
```

Build (i.e. actually run the benchmarks):
```
[atkins3@rhea-login4g build]$ make
Scanning dependencies of target xgc-restart-run-and-wait
Submitting ./2048-processes-bp4
Submitting ./512-processes-bp4
Submitting ./128-processes-bp4

2020-09-03 22:02:23.730857124
atkins3/2048-processes-bp4 : NOT STARTED
atkins3/512-processes-bp4 : NOT STARTED
atkins3/128-processes-bp4 : NOT STARTED

2020-09-03 22:02:42.837833569
atkins3/2048-processes-bp4 : NOT STARTED
atkins3/512-processes-bp4 : NOT STARTED
atkins3/128-processes-bp4 : NOT STARTED
...

2020-09-03 22:09:05.406733666
atkins3/2048-processes-bp4 : NOT STARTED
atkins3/512-processes-bp4 : IN PROGRESS, job 94109 , 0 / 1
atkins3/128-processes-bp4 : NOT STARTED
...

2020-09-03 22:18:21.392559179
atkins3/2048-processes-bp4 : NOT STARTED
atkins3/512-processes-bp4 : DONE, 1 / 1 failed
atkins3/128-processes-bp4 : IN PROGRESS, job 94110 , 0 / 1
...

2020-09-04 00:42:46.842468711
atkins3/2048-processes-bp4 : IN PROGRESS, job 94108 , 0 / 1
atkins3/512-processes-bp4 : DONE, 1 / 1 failed
atkins3/128-processes-bp4 : DONE

2020-09-04 00:43:02.339116247
atkins3/2048-processes-bp4 : DONE, 1 / 1 failed
atkins3/512-processes-bp4 : DONE, 1 / 1 failed
atkins3/128-processes-bp4 : DONE
WARNING: At least one of the jobs have failed
Built target xgc-restart-run-and-wait
Scanning dependencies of target xgc-restart-generate-reports
INFO: :Campaign directory: /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart, user script: /ccs/home/atkins3/adios2-testing/source/performance/xgc-restart/parse_timings.py, tau metric collection: True, output report in: campaign_results.csv
INFO: :Parsing campaign /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart
INFO: :Parsing sweep groups for atkins3
INFO: :Parsing sweep group /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/2048-processes-bp4
INFO: :Parsing run /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/2048-processes-bp4/run-0.iteration-0
ERROR: Could not find codar.workflow.stdout.reader
INFO: :Parsing sweep group /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/512-processes-bp4
INFO: :Parsing run /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/512-processes-bp4/run-0.iteration-0
INFO: :Parsing sweep group /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/128-processes-bp4
INFO: :Parsing run /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/128-processes-bp4/run-0.iteration-0
INFO: :Done generating report.
INFO: :Writing output to campaign_results.csv
Built target xgc-restart-generate-reports
[atkins3@rhea-login4g build]$ 
```

Test (collect per-group statistics):
```
[atkins3@rhea-login4g build]$ ctest -VV
UpdateCTestConfiguration  from :/ccs/home/atkins3/adios2-testing/build/DartConfiguration.tcl
Parse Config file:/ccs/home/atkins3/adios2-testing/build/DartConfiguration.tcl
UpdateCTestConfiguration  from :/ccs/home/atkins3/adios2-testing/build/DartConfiguration.tcl
Parse Config file:/ccs/home/atkins3/adios2-testing/build/DartConfiguration.tcl
Test project /ccs/home/atkins3/adios2-testing/build
Constructing a list of tests
Done constructing a list of tests
Updating test list for fixtures
Added 0 tests to meet fixture requirements
Checking test dependency graph...
Checking test dependency graph end
test 1
    Start 1: xgc-restart-128-processes-bp4

1: Test command: /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/cheetah-group-stats.sh "/gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/128-processes-bp4"
1: Test timeout computed to be: 1500
1: CTEST_FULL_OUTPUT
1: 
1:     Open Input Stream xgc.restart.00040.bp... 
1:     Open Input Stream xgc.restart.00040.bp... 
1:     Open Input Stream xgc.restart.00040.bp... 
...
1:     Open Input Stream xgc.restart.00040.bp... 
1:     App 1: Max read time = 42.4156
1:     App 1: Min read time = 21.8557
1: App 1 Step 2: 
1: ADIOS IOTEST App 1 total time 42.4601 seconds 
1: App 1 Step 1: 
1:     App 1: Max write time = 32.2589
1:     App 1: Min write time = 25.0823
1: ADIOS IOTEST App 1 total time 34.1824 seconds 
1: atkins3/128-processes-bp4 : DONE
1:   run-0.iteration-0: done; succeeded
1:     writer: 0
1:     reader: 0
1: 
1: >>> run-0.iteration-0 post-process stdout (0 bytes)
1: 
1: >>> run-0.iteration-0 post-process stderr (0 bytes)
1: 
1: >>> run-0.iteration-0 reader stdout (6163 bytes)
1: 
1: >>> run-0.iteration-0 reader stderr (0 bytes)
1: 
1: >>> run-0.iteration-0 writer stdout (134 bytes)
1: 
1: >>> run-0.iteration-0 writer stderr (0 bytes)
1: 
1: 
1: ----------------------------------------
1: CDash Measurements
1: ----------------------------------------
1: 
1: Procesing run-0.iteration-0
1: <DartMeasurement type="numeric/double" name="writer_time_stdout_min">34.182400</DartMeasurement>
1: <DartMeasurement type="numeric/double" name="writer_time_stdout_max">34.182400</DartMeasurement>
1: <DartMeasurement type="numeric/double" name="writer_time_stdout_mean">34.182400</DartMeasurement>
1: <DartMeasurement type="numeric/double" name="reader_time_stdout_min">42.460100</DartMeasurement>
1: <DartMeasurement type="numeric/double" name="reader_time_stdout_max">42.460100</DartMeasurement>
1: <DartMeasurement type="numeric/double" name="reader_time_stdout_mean">42.460100</DartMeasurement>
1/3 Test #1: xgc-restart-128-processes-bp4 ....   Passed   48.88 sec
    Start 2: xgc-restart-2048-processes-bp4

2: Test command: /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/cheetah-group-stats.sh "/gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/2048-processes-bp4"
2: Test timeout computed to be: 1500
2: CTEST_FULL_OUTPUT
2: 
2: App 1 Step 1: 
2: ----------------------------------------
2: CDash Measurements
2: ----------------------------------------
2: 
2: Procesing run-0.iteration-0
2: Skipping due to invalid numeric value(s) for one or more measurements
2/3 Test #2: xgc-restart-2048-processes-bp4 ...   Passed   11.60 sec
test 3
    Start 3: xgc-restart-512-processes-bp4

3: Test command: /gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/cheetah-group-stats.sh "/gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart/atkins3/512-processes-bp4"
3: Test timeout computed to be: 1500
3: CTEST_FULL_OUTPUT
3: 
...
3: ----------------------------------------
3: CDash Measurements
3: ----------------------------------------
3: 
3: Procesing run-0.iteration-0
3: Skipping due to invalid numeric value(s) for one or more measurements
3/3 Test #3: xgc-restart-512-processes-bp4 ....   Passed   23.78 sec

100% tests passed, 0 tests failed out of 3

Total Test time (real) =  84.35 sec
[atkins3@rhea-login4g build]$
```

In this case 2 of the three performance benchmarks actually failed; the full output is in each tests and can be used to try to diagnose the problem.  

### CTest Example 2: Running the benchmarks and submitting to the dashboard

```
[atkins3@rhea-login4g build]$ cmake -DSITE=rhea -DBUILDNAME=adios2-default -DMACHINE=rhea -DTEST_OUTPUT_BASE_DIR=${MEMBERWORK}/csc303/performance-testing/rhea/tmp-test ../source/performance
Using ENV_SETUP="/ccs/home/atkins3/adios2-testing/source/performance/xgc-restart/env-setup/env_setup_rhea.sh"
-- Locating cheetah...
-- Locating cheetah... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/codar-cheetah-develop-zotwnryl3hox2iylnofurbbo6r3e3y6n/bin/cheetah
-- Locating tau_exec...
-- Locating tau_exec... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/tau-2.29-tc3ik7ihp5p5sz6q42gmysr3vcs34xme/bin/tau_exec
-- Locating bpls...
-- Locating bpls... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/adios2-master-qu6mjxrg7vmpom7w7nh5wxixmgrdm22a/bin/bpls
-- Locating adios2_iotest...
-- Locating adios2_iotest... /autofs/nccs-svm1_proj/csc303/adios2-test-suite/rhea/spack/opt/spack/linux-rhel7-sandybridge/gcc-8.4.0/adios2-master-qu6mjxrg7vmpom7w7nh5wxixmgrdm22a/bin/adios2_iotest
Generating xgc-restart test scripts in "/gpfs/alpine/scratch/atkins3/csc303/performance-testing/rhea/tmp-test/xgc-restart"
--   Generating campaing configuration
--   Generating run scripts
--   Generating full cheetah campaign
-- Adding test group: xgc-restart-128-processes-bp4
-- Adding test group: xgc-restart-2048-processes-bp4
-- Adding test group: xgc-restart-512-processes-bp4
-- Configuring done
-- Generating done
-- Build files have been written to: /ccs/home/atkins3/adios2-testing/build
[atkins3@rhea-login4g build]$
[atkins3@rhea-login4g build]$ make Experimental
Scanning dependencies of target Experimental
   Site: rhea
   Build name: adios2-default
Create new tag: 20200904-1520 - Experimental
Configure project
   Each . represents 1024 bytes of output
    ..chat.google.com Size of output: 1K
Build project
   Each symbol represents 1024 bytes of output.
   '!' represents an error and '*' a warning.
    ..*. Size of output: 3K
   0 Compiler errors
   1 Compiler warnings
Test project /ccs/home/atkins3/adios2-testing/build
    Start 1: xgc-restart-128-processes-bp4
1/3 Test #1: xgc-restart-128-processes-bp4 ....   Passed   30.09 sec
    Start 2: xgc-restart-2048-processes-bp4
2/3 Test #2: xgc-restart-2048-processes-bp4 ...   Passed   37.49 sec
    Start 3: xgc-restart-512-processes-bp4
3/3 Test #3: xgc-restart-512-processes-bp4 ....   Passed  194.47 sec

100% tests passed, 0 tests failed out of 3

Total Test time (real) = 262.26 sec
Performing coverage
 Cannot find any coverage files. Ignoring Coverage request.
Submit files
   SubmitURL: http://open.cdash.org/submit.php?project=ADIOS2-Testing
   Uploaded: /ccs/home/atkins3/adios2-testing/build/Testing/20200904-1520/Configure.xml
   Uploaded: /ccs/home/atkins3/adios2-testing/build/Testing/20200904-1520/Build.xml
   Uploaded: /ccs/home/atkins3/adios2-testing/build/Testing/20200904-1520/Test.xml
   Uploaded: /ccs/home/atkins3/adios2-testing/build/Testing/20200904-1520/Done.xml
   Submission successful
Built target Experimental
[atkins3@rhea-login4g build]$
```

The results should now be visible on the public dashboard at https://open.cdash.org/index.php?project=ADIOS2-Testing
