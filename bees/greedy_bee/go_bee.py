#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
from bees_greedy import BeeWanderGreedy



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--runtime', type=int, default=25)
    parser.add_argument('-b', '--num-bees', type=int, default=3)

    args = parser.parse_args()

    # 1. connect
    bees = []
    for i in range(1, args.num_bees+1):
        bees.append(BeeWanderGreedy('Bee-{:03d}'.format(i)))
    print('All bees connected!')
    # 2. move
    # - the bee moves by default

    # Prevent the program from exiting for specified runtime
    try:
        start = time.time()
        i = 0
        while (args.runtime == 0) or (time.time() - start < args.runtime):
            #for b in bees:
            #    b.climb()
            time.sleep(0.20)
            i += 1
            if i % (20*3) == 0:
                print "[i] {:.3f} elapsed".format(time.time() - start)

        for b in bees:
            b.stop()
    except KeyboardInterrupt:
        for b in bees:
            b.stop()


