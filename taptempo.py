#!/usr/bin/env python

from __future__ import print_function

import tty
import termios
from time import time
from sys import stdin


def getchar():
    fd = stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(stdin.fileno())
        ch = stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def addtime(times):
    if type(times) != list:
        raise(TypeError)
    t = time()
    if len(times) == 0:
        tdiff = 0
    else:
        tdiff = t - times[-1][0]
    return (t, tdiff)


print('Tap a key on each beat. Press q to quit.')

TIMES = []
while True:
    char = getchar()
    if char in ('q', 'Q', '\x1b', '\x03'):  # q, Q, ESC, Control+C
        print()
        quit()

    TIMES.append(addtime(TIMES))
    if len(TIMES) > 16:
        del TIMES[0]
    if len(TIMES) > 1:
        if TIMES[0][1] == 0:
            del TIMES[0]
        averagetime = sum([row[1] for row in TIMES])/float(len(TIMES))
        bpm = (1.0/(averagetime/60.0))

        print("\nDetected BPM: %0.3f (Avg time between each: %0.3fs)"
              % (bpm, averagetime), end='')
