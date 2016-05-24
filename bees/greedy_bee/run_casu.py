#!/usr/bin/env python
# -*- coding: utf-8 -*-


from assisipy import casu
import time

import argparse

MIN_TEMP = 25.0
MAX_TEMP = 50.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    '''
    set temps of a series of CASU controllers, just outside the
    arena wall, so temperature is felt inside but the casu bodies
    do not influence directional changes.

    ''')
    parser.add_argument('-c', '--num-casus', type=int, default=3)
    parser.add_argument('-rt', '--right-temp', type=float, default=28.0)
    parser.add_argument('-lt', '--left-temp',  type=float, default=45.0)
    parser.add_argument('-t', '--runtime', type=int, default=60)
    args = parser.parse_args()

    # connect to all of the CASUs
    l_casus = []
    r_casus = []
    for i in xrange(0, args.num_casus):
        side = 'l'
        cname = 'casu-{}0{}'.format(side, i)
        c = casu.Casu(name=cname)
        l_casus.append(c)

        side = 'r'
        cname = 'casu-{}0{}'.format(side, i)
        c = casu.Casu(name=cname)
        r_casus.append(c)

    # set temp as desired
    start = time.time()


    # turn the temperature up
    try:
        i = 0
        for c in l_casus:
            clr = (args.left_temp -MIN_TEMP) / (MAX_TEMP - MIN_TEMP)
            c.set_temp(args.left_temp)
            c.set_diagnostic_led_rgb(clr, 0, 0)
        for c in r_casus:
            c.set_temp(args.right_temp)
            clr = (args.right_temp -MIN_TEMP) / (MAX_TEMP - MIN_TEMP)
            c.set_diagnostic_led_rgb(clr, 0, 0)

        while (args.runtime == 0) or (time.time() - start < args.runtime):
            i += 1
            time.sleep(0.25)
            if i % 20 == 0:
                print "[{}] L: {:.3f} R: {:.3f}".format(i, l_casus[0].get_temp(casu.TEMP_TOP), r_casus[0].get_temp(casu.TEMP_TOP))

        # wait for interrupt
    except KeyboardInterrupt:
        # disconnect the casus
        for c in l_casus + r_casus:
            c.set_diagnostic_led_rgb(0.4, 0.4, 0.4)
            c.stop()


