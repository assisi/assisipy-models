#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Identical controllers for multiple bees.
"""

from assisipy import bee

import threading
import argparse
import time


class BeeWanderGreedy(object):
    """
    An example of gradient-climbing wandering bee controller,
    based on the "wanderingbee" controller from assisi/examples repo

    Written

    """

    def __init__(self, bee_name):
        self.__bee = bee.Bee(name = bee_name)
        self.name = bee_name
        self.__thread = threading.Thread(target=self.climb)
        self.__thread.daemon = True
        self.__thread.start()
        self.max_turn = 2.0
        self.max_grad = 0.5

    def go_straight(self, v = 2.0):
        self.__bee.set_vel(v, v)

    def turn_left(self, rv  = 1.0):
        self.__bee.set_vel(-rv, rv)

    def stop(self):
        self.__bee.set_vel(0, 0)

    def turn_right(self, rv=1.0):
        self.__bee.set_vel(rv, -rv)

    def climb(self):
        """
        attempt to follow gradients in environment
        """
        last_report = time.time()
        while True:
            self.go_straight()
            now = time.time()

            # avoid obstacle
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_RIGHT_FRONT) < 4)):
                self.turn_left()
            while ((self.__bee.get_range(bee.OBJECT_FRONT) < 3)
                   and (self.__bee.get_range(bee.OBJECT_LEFT_FRONT) < 4)):
                self.turn_right()
            # follow gradient
            T_left  = self.__bee.get_temp(bee.TEMP_SENSOR_LEFT)
            T_right = self.__bee.get_temp(bee.TEMP_SENSOR_RIGHT)
            lr_grad = T_right - T_left
            sgn = 1.0 if lr_grad > 0 else -1.0
            mag = min(abs(lr_grad), self.max_grad)
            rv = sgn * (mag / self.max_grad * self.max_turn)
            if now - last_report > 5:
                temps = self.__bee.get_temp(bee.ARRAY)
                tstr = ", ".join(["{:.2f}".format(t) for t in temps])
                print self.name + ":\t" + tstr
                last_report = now
                print "L {:.2f} R {:.2f}: {:.3f}".format(T_left, T_right, rv)

            self.turn_right(rv = rv)
            #self.max_turn = 0.5
            #self.max_grad = 2.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--runtime', type=int, default=25)
    parser.add_argument('-b', '--num-bees', type=int, default=3)
    args = parser.parse_args()

    # Spawn the bees at randomly generated poses and let them run :)
    bees = []
    for i in range(1, args.num_bees+1):
        bees.append(BeeWanderGreedy('Bee-{:03d}'.format(i)))

    print('All bees connected!')

    # Prevent the program from exiting
    try:
        while True:
            time.sleep(0.25)

    except KeyboardInterrupt:
        # disconnect the bees
        for b in bees:
            b.stop()

