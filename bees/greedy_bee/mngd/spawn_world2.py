#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import pi, cos, sin
from assisipy import sim
import argparse
import random
from assisipy_utils import arena
from assisipy_utils.mgmt import specs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    '''
    Create a circular wall with some casus outside of the wall,
    and spawn bees
    ''')
    parser.add_argument('-b', '--num-bees', type=int, default=0)
    parser.add_argument('-c', '--num-casus', type=int, default=3)
    parser.add_argument('-r', '--radius', type=float, default=12)
    parser.add_argument('-ol', '--obj-listing', type=str, default=None,
                        help='name of file to list all of the spawned bee details')
    parser.add_argument('-e', '--exec-script', type=str, required=True,
                        help='name of script to execute for each bee in `bee-file`')

    args = parser.parse_args()
    obj_file = None
    if args.obj_listing is not None:
        obj_file = open(args.obj_listing, 'w')


    simctrl = sim.Control()

    conf = None
    if args.num_bees > 0:
        for i in range(1, args.num_bees+1):
            name = 'Bee-{:03d}'.format(i)

            pose = (random.uniform(-4, 4), random.uniform(-4, 4),
                    2*pi*random.random())

            simctrl.spawn('Bee', name, pose)
            print 'Spawned bee', name
            if obj_file:
                s = specs.gen_spec_str_yaml(name, 'Bee', pose,
                                            args.exec_script, conf,
                                            'tcp://localhost:5556',
                                            'tcp://localhost:5555',
                                            )
                obj_file.write(s + "\n")


    stp = pi / 8.0
    for i in range(0, args.num_casus):
        thetal = pi - (stp*(args.num_casus-1)/2) + (i * stp)
        thetar = thetal + pi
        for theta, side in zip([thetal, thetar], 'lr'):
            cname = 'casu-{}0{}'.format(side, i)
            x = (args.radius + 1.0) * cos(theta)
            y = (args.radius + 1.0) * sin(theta)
            pos = (x, y, 0)
            simctrl.spawn('Casu', cname, pos)

    A = arena.CircleArena(radius=args.radius)
    A.spawn(simctrl)




