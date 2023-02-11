import x68k
import machine
import time
import random

from struct import pack

# GPIP register
REG_GPIP = const(0xE88001)

# maze size
MAZE_WIDTH  = 63
MAZE_HEIGHT = 63

# digging
def dig(maze, pos, g=None):

  # dig position
  (x, y) = pos

  # possible digging directions
  ds = []       
  if y > 1 and maze[ (y - 1) * MAZE_WIDTH + x ] and maze[ (y - 2) * MAZE_WIDTH + x ]:
    ds.append(0)
  if x > 1 and maze[ y * MAZE_WIDTH + x - 1 ] and maze[ y * MAZE_WIDTH + x - 2 ]:
    ds.append(1)
  if y < MAZE_HEIGHT - 2 and maze[ (y + 1) * MAZE_WIDTH + x ] and maze[ (y + 2) * MAZE_WIDTH + x ]:
    ds.append(2)
  if x < MAZE_WIDTH - 2 and maze[ y * MAZE_WIDTH + x + 1 ] and maze[ y * MAZE_WIDTH + x + 2 ]:
    ds.append(3)

  # no more direction
  if not ds:
    return None

  # dig
  d = random.choice(ds)
  if d == 0:    # up
    maze[ (y - 1) * MAZE_WIDTH + x ] = 0
    maze[ (y - 2) * MAZE_WIDTH + x ] = 0
    if g:
      g.fill( 8 + x * 16, 8 + (y - 2) * 16, 8 + x * 16 + 15, 8 + (y - 1) * 16 + 15, 0)
    y -= 2
  elif d == 1:  # left
    maze[ y * MAZE_WIDTH + x - 1 ] = 0
    maze[ y * MAZE_WIDTH + x - 2 ] = 0
    if g:
      g.fill( 8 + (x - 2) * 16, 8 + y * 16, 8 + (x - 1) * 16 + 15, 8 + y * 16 + 15, 0)
    x -= 2
  elif d == 2:  # down
    maze[ (y + 1) * MAZE_WIDTH + x ] = 0
    maze[ (y + 2) * MAZE_WIDTH + x ] = 0
    if g:
      g.fill( 8 + x * 16, 8 + (y + 1) * 16, 8 + x * 16 + 15, 8 + (y + 2) * 16 + 15, 0)
    y += 2
  elif d == 3:  # right
    maze[ y * MAZE_WIDTH + x + 1 ] = 0
    maze[ y * MAZE_WIDTH + x + 2 ] = 0
    if g:
      g.fill( 8 + (x + 1) * 16, 8 + y * 16, 8 + (x + 2) * 16 + 15, 8 + y * 16 + 15, 0)
    x += 2

  # return new dig position
  return (x, y)

# main
def main():

  # randomize
  random.seed(int(time.time() * 10))

  # initialize screen
  x68k.crtmod(16, True)
  x68k.iocs(x68k.i.OS_CUROF)
  x68k.iocs(x68k.i.TXFILL,a1=pack('6h',0,0,0,1024,1024,0))
  x68k.iocs(x68k.i.TXFILL,a1=pack('6h',1,0,0,1024,1024,0))
  g0 = x68k.GVRam(0)
  g0.window(0, 0, 1023, 1023)
  g0.fill(0, 0, 1023, 1023, 0)
  x68k.vpage(1)
  
  # scroll direction patterns
  dx = [ 1, 0, -1,  0, 1,  1, -1, -1 ]
  dy = [ 0, 1,  0, -1, 1, -1,  1, -1 ]

  # main loop up to 16 times
  for i in range(16):

    # initialize maze
    maze = [ 1 ] * MAZE_WIDTH * MAZE_HEIGHT

    # select initial digging position
    x0 = random.randrange(1, MAZE_WIDTH  - 2, 2)     # initial X
    y0 = random.randrange(1, MAZE_HEIGHT - 2, 2)     # initial Y
    pos = (x0, y0)
    
    # dig point candidates
    dig_positions = [ pos ]

    # initialize graphic page
    g0.fill(0, 0, 1023, 1023, random.randrange(2, 14, 2))
    g0_x = 0
    g0_y = 0  
    g0.home(g0_x, g0_y)

    # dig
    while True:

      # check shift key to exit
      if x68k.iocs(x68k.i.B_SFTSNS) & 0x01:
        i = 999
        break

      # dig ops
      next_pos = dig(maze, pos, g0)       # dig and get the next position
      if next_pos is not None:            # if next position is available  
        pos = next_pos                    # continue to dig
        dig_positions.append(next_pos)    # remember as future potential dig position
      else:                               # if we cannot dig with the current position, back to previous positions
        if not dig_positions:             # if no more dig position
          break                           # digging complete
        pos = dig_positions.pop()         # pop from the candidate position list

      # graphic scroll
      with x68k.Super():  
        g0_x = (g0_x + dx[i % 8] + 1024) % 1024
        g0_y = (g0_y + dy[i % 8] + 1024) % 1024
        while (machine.mem8[ REG_GPIP ] & 0x10) == 0:
          pass
        while (machine.mem8[ REG_GPIP ] & 0x10) != 0:
          pass
        g0.home(g0_x, g0_y)

    # abort check
    if i >= 999:
      break

    # maze complete
    g0.home(0, 0)
    time.sleep(3)

  # cursor on
  x68k.iocs(x68k.i.OS_CURON)

if __name__ == "__main__":
  main()