# EFFIS code coupling scenarios with adios\_iotest utility.
Coupling scenarios:

1. **XG** Bidirectional coupling between X and G. 
2. **XGN** Same as XG but there is a third app doing nothing. This throws off engines relying on the world communicator.
3. **XCG** Separate coupler code C receives data from X and G and interpolates data and sends the other party. Coupling pattern:
    * G sends density to C
    * C interpolates data and sends to X
    * X receives density from C and computes field
    * X sends field to C and continues next computation loop
    * C interpolates data and sends to G
    * G continues next computation loop

In all cases, G determines the number of coupling steps (see first command **steps** in the config (.txt) files).

    
## Usage
Use the script **effis__coupling.sh** to run one of the scenarios. 

Usage: 
* ./effis-coupling.sh setup nprocs1 nprocs2 nprocs3

Setups: 
* xg xgn xcg

Example: Run X on 4 processes, C on 1 and G on 2 processes:
* ./effis-coupling.sh xcg 4 1 2 

## Manual runs
Instead of the script, one can construct the `adios_iotest` commands and launch them separately (SST, BP4), or together in MPMD mode (required for SSC and InSituMPI).

```
$ N1=4
$ N2=1
$ N3=2
$ CFG=effis-coupling-xcg.txt 
$ XML=effis-coupling-xcg.xml
$ IOTEST=adios_iotest
$ mpirun -n $N1 $IOTEST  -a 1 -c $CFG -x $XML -s -t -d $N1 1 1 : \
         -n $N2 $IOTEST  -a 2 -c $CFG -x $XML -s -t -d $N2 1 1 : \
         -n $N3 $IOTEST  -a 3 -c $CFG -x $XML -s -t -d $N3 1 1
```

## Example
```
$ ./effis-coupling.sh xcg 4 1 2
Run EFFIS coupling
Exe:  	 /home/pnb/work/ADIOS2/build/bin/adios_iotest
Setup:	 xcg
XGC:	 4 processes
COUPLER:	 2 processes
GENE:	 1 processes
mpirun -n 4 /home/pnb/work/ADIOS2/build/bin/adios_iotest -a 1 -c effis-coupling-xcg.txt -x effis-coupling-xcg.xml -s -t -d 4 1 1 : -n 2 /home/pnb/work/ADIOS2/build/bin/adios_iotest -a 2 -c effis-coupling-xcg.txt -x effis-coupling-xcg.xml -s -t -d 2 1 1 : -n 1 /home/pnb/work/ADIOS2/build/bin/adios_iotest -a 3 -c effis-coupling-xcg.txt -x effis-coupling-xcg.xml -s -t -d 1 1 1
App 1 Step 1: 
App 2 Step 1: 
App 3 Step 1: 
    App 3: Max write time = 0.0937838
    App 3: Min write time = 0.0937838
    App 2: Max read time = 2.19494
    App 2: Min read time = 2.18129
    App 2: Max write time = 0.0555778
    App 2: Min write time = 0.053401
    App 1: Max read time = 2.1134
    App 1: Min read time = 2.10112
    App 1: Max write time = 0.0371355
    App 1: Min write time = 0.0357138
App 1 Step 2: 
    App 2: Max read time = 1.22793
    App 2: Min read time = 1.2236
    App 2: Max write time = 0.0693103
    App 2: Min write time = 0.0666912
App 2 Step 2: 
    App 3: Max read time = 2.44992
    App 3: Min read time = 2.44992
App 3 Step 2: 
    App 3: Max write time = 0.103451
    App 3: Min write time = 0.103451
    App 2: Max read time = 2.16883
    App 2: Min read time = 2.16573
    App 2: Max write time = 0.0644515
    App 2: Min write time = 0.0604229
    App 1: Max read time = 2.09693
    App 1: Min read time = 2.08408
    App 1: Max write time = 0.0387287
    App 1: Min write time = 0.0372128
App 1 Step 3: 
    App 2: Max read time = 1.19519
    App 2: Min read time = 1.19162
    App 2: Max write time = 0.0738095
    App 2: Min write time = 0.0735832
App 2 Step 3: 
    App 3: Max read time = 3.37114
    App 3: Min read time = 3.37114
App 3 Step 3: 
    App 3: Max write time = 0.0725487
    App 3: Min write time = 0.0725487
    App 2: Max read time = 2.16671
    App 2: Min read time = 2.16451
    App 2: Max write time = 0.0463034
    App 2: Min write time = 0.0458422
    App 1: Max read time = 3.09643
    App 1: Min read time = 3.08436
    App 1: Max write time = 0.0303853
    App 1: Min write time = 0.0286744
App 1 Step 4: 
    App 2: Max read time = 2.20579
    App 2: Min read time = 2.20254
    App 2: Max write time = 0.0594265
    App 2: Min write time = 0.0560425
App 2 Step 4: 
    App 3: Max read time = 3.37567
    App 3: Min read time = 3.37567
```

Result files: 
```
G_to_C.bp
C_to_X.bp
C_to_G.bp
X_to_C.bp
```

```
$ bpls -l G_to_C.bp
  double   density  3*{210943, 32} = 0 / 1.2
$ bpls -l C_to_X.bp/
  double   density  3*{210943, 32} = 0 / 1.2
$ bpls -l X_to_C.bp/
  double   field  3*{263243, 32} = 0 / 3.002
$ bpls -l C_to_G.bp/
  double   field  3*{263243, 32} = 0 / 3.002
```

