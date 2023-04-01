#
#  s44shuff.py - S44/A44 shuffle player on MicroPython for X680x0
#

import x68k
import os
import sys
import time
import random
from struct import pack
from uctypes import addressof

# extract wild card file names
def list_files(wildcard_name):

  files = []

  filbuf = bytearray(53)
  if x68k.dos(x68k.d.FILES,pack('llh',addressof(filbuf),addressof(wildcard_name),0x20)) < 0:
    return files

  while True:

    name = filbuf[30:53]
    for i in range(len(name)):
      if name[i] == 0x00:
        name = name[:i]
        break

    files.append(name.decode())

    if x68k.dos(x68k.d.NFILES,pack('l',addressof(filbuf))) < 0:
      break

  return files
  
def main():

  # randomize
  random.seed(int(time.time() * 10))

  # list s44/a44 files in the current directory
  files = list_files(".\\*.s44") + list_files(".\\*.a44")

  # loop count
  loop_count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
  
  # loop cancel flag
  terminate = False

  # main loop
  for i in range(loop_count):

    # shuffle files
    for i in range(len(files)*3):
      a = random.randint(0,len(files)-1)
      b = random.randint(0,len(files)-1)
      f = files[a]
      files[a] = files[b]
      files[b] = f

    # execute mp3exp as a child process
    for f in files:
      x68k.crtmod(16,True)            # reset screen
      cmd = f"mp3exp -x -t75 {f}"
      print(f"COMMAND: {cmd}\n")
      if os.system(cmd) != 0:
        terminate = True
        break

    # abort check
    if terminate:
      break

if __name__ == "__main__":
  main()
