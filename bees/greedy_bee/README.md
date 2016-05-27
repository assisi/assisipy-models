A basic gradient-following agent bee behavioural model
======================================================

This example shows a bee behavioural model that is capable of following
gradients in its local thermal environment.  The dependencies include

- `assisipy` 
- `assisipy_utils`
- everything else is python builtin (argparse, random, threading, time)

To run -- simpler version
-------------------------

The programs have default values that work together, but options are given.
All the python scripts have `-<short>` and `--<long-version>` arguments; type
`./<scriptname> -h` to see more detail.

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



------------------------------------
To run -- more managed automatically
------------------------------------

This illustrates how specifications can be written -- note! the absolute latest 
version of assisipy-utils is required for the yaml-parsing version. It will be 
part of v0.6.0 but at present should be installed by github@dev.

0. cd mngd

1. as per #1 above

    assisi_playground &

2. Spawn the casus (3 each side), arena boundary (11cm), and bees (6)

    ./spawn_world2.py -r 16 -b 6 -c 2 -ol greedybees.yml -e bees_greedy2.py

3. as per #3 above

    ./run_casu.py -c 2 -lt 45 -rt 29 -t 0

4. in a second terminal window, run the bee behaviour. 

    run_multiagent -ol greedybees.yml --logpath /tmp/test_greedy_bees

    press <ctrl-c> to terminate the bee behaviour controllers.


Forthcoming in this example:
- configuration files setting the bee behaviour
- integration with deployment tools for the casus (needs a bit more work on 
  autogen of msg addresses & not sure how to do cleanly for the different 
  physical vs simulated scenarios)

