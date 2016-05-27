#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Identical controllers for multiple bees. They go uphill in thermal gradients
as measured across their body.

This variant uses the assisipy_utils behaviour running framework,
and not threading

"""

from assisipy import bee
import os, yaml
import time
from assisipy_utils.common import beelib

class BeeWanderGreedy(object):
    """
    An example of gradient-climbing wandering bee controller,
    based on a combination of "wanderingbee" controller (assisi/examples)
    and "basic_bee_fwd" from assisipy-utils repo


    """
    #{{{ initialiser
    def __init__(self, bee_name, logfile, pub_addr, sub_addr, conf_file=None,
                 verb=False):

        # process the input arguments and config file.
        self.bee_name = bee_name
        if conf_file is not None and conf_file != 'null' and conf_file != 'None':
            with open(conf_file, 'r') as f:
                conf = yaml.safe_load(f)
        else:
            conf = {}
        self.override_fwd_clr = conf.get('override_fwd_clr', False)
        self._fwd_clr         = conf.get('fwd_clr', (0.3,0.3,0.3))
        self.max_turn         = 2.0 # TODO: from cfg file?
        self.max_grad         = 0.5 # TODO: from cfg file?
        self.verb = verb

        if self.verb:
            print "attempting to connect to bee with name %s" % bee_name
            print "\tpub_addr:{}".format(pub_addr)
            print "\tsub_addr:{}".format(sub_addr)

        '''
        instantiates a assisipy.bee object but not derived from bee (At present)
        default settings are 2nd argument, if not set by config file
        '''
        self.__bee = bee.Bee(name=self.bee_name, pub_addr=pub_addr,
                             sub_addr=sub_addr)

        # easiest way to show something about the bee state is through colour
        self.CLR_FWD  = (0.93, 0.79, 0)
        self.CLR_COLL_OBJ  = (0, 0, 1)
        self.CLR_COLL_BEE  = (0, 1, 0)
        self.CLR_WAIT  = (0.93, 0.0, 0)

        if self.override_fwd_clr:
            # special color for this bee from config file
            c = [float(n) for  n in self._fwd_clr.strip('()').split(',')]
            self.CLR_FWD = c

        self.__bee.set_color(*self.CLR_FWD)
        self.last_turn_time = time.time()
        self.last_report = time.time()
    #}}}

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
        if now - self.last_report > 5:
            temps = self.__bee.get_temp(bee.ARRAY)
            tstr = ", ".join(["{:.2f}".format(t) for t in temps])
            print self.bee_name + ":\t" + tstr
            self.last_report = now
            print "L {:.2f} R {:.2f}: {:.3f}".format(T_left, T_right, rv)

            self.turn_right(rv = rv)


if __name__ == "__main__":
    # handle command-line arguments
    parser = beelib.default_parser()
    args = parser.parse_args()

    # set up the bee behaviour, including attaching to simulator
    logfile = os.path.join(args.logpath, "bee_track-{}.csv".format(args.bee_name))
    the_bee = BeeWanderGreedy(
        bee_name=args.bee_name, logfile = logfile,
        pub_addr=args.pub_addr, sub_addr=args.sub_addr,
        conf_file=args.conf_file,)

    # run handler until keyboard interrupt. (or other SIGINT)
    try:
        while True:
            time.sleep(0.2)
            the_bee.climb()
    except KeyboardInterrupt:
        print "shutting down bee {}".format(args.bee_name)
        the_bee.stop()
