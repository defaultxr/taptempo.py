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
        tdiff = 0  # initial seed
    else:
        tdiff = t - times[-1][0]
    return (t, tdiff)


def averagetimes(times):
    averagetime = sum([row[1] for row in times])/float(len(times))
    bpm = (1.0/(averagetime/60.0))
    return (averagetime, bpm)


def main():
    print('Tap a key on each beat. Press q to quit.', end='\r')

    times = []
    while True:
        char = getchar()
        if char in ('q', 'Q', '\x1b', '\x03'):  # q, Q, ESC, Control+C
            print()
            quit()

        times.append(addtime(times))
        if len(times) > 1:
            # remove first element if it's either the initial seed
            # or when the list reaches max length
            if times[0][1] == 0 or len(times) > 16:
                del times[0]
            (averagetime, bpm) = averagetimes(times)

            print("\rDetected BPM: %7.3f (Avg time between each: %0.3fs)"
                  % (bpm, averagetime), end='')


if __name__ == '__main__':
    main()
