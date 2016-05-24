A basic gradient-following agent bee behavioural model
======================================================

This example shows a bee behavioural model that is capable of following
gradients in its local thermal environment.  The dependencies include

- `assisipy` 
- `assisipy_utils`
- everything else is python builtin (argparse, random, threading, time)

To run
------

The programs have default values that work together, but options are given.
All the python scripts have -<short> and --<long-version> arguments; type
./<scriptname> -h to see more detail.

1. launch a playground instance

    assisi_playground &

2. Spawn the casus (3 each side), arena boundary (11cm), and bees (6)

    ./spawn_world.py -r 16 -b 6 -c 2

3. set temperatures on the casus, hot on the left and cooler on right,
   to run indefinitely.

    ./run_casu.py -c 2 -lt 45 -rt 29 -t 0
    
    press <ctrl-c> to terminate the CASU controllers cleanly.

4. in a second terminal window, run the bee behaviour. 

    ./run_bees.py -b 6

    press <ctrl-c> to terminate the bee behaviour controllers.


