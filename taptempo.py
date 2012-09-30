#!/usr/bin/env python
import tty, termios
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

if __name__ == '__main__':
 print('Tap a key on each beat. Press q to quit.', end='\r')
 array = []

 while True:
  char = getchar()
  if char in ('q', 'Q', '\x1b', '\x03'): # q, Q, ESC, Control+C
   quit()
  else:
   array.append(time())
   if len(array) > 4:
    del array[0]
   if len(array) < 2:
    print('Keep tapping on the beats. Press q to quit.', end='\r')
   else:
    averagetime = 0
    for i in range(len(array)-1):
     averagetime += (array[i+1]-array[i])
    averagetime = averagetime / ( (len(array)-1) * 4)
    averagetime *= 1000
    bpm = (60000.0/averagetime)/4.0
    print("\rDetected BPM: %.3f (Avg time between each: %.3fms)" % (bpm, averagetime), end='')
