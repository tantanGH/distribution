import x68k
import machine
import time
import random

from struct import pack

# maze size
MAZE_WIDTH  = const(63)
MAZE_HEIGHT = const(63)

class Maze:

  # constructor
  def __init__(self, width, height, g=None):

    self.width = width
    self.height = height
    self.g = g

    self.scroll_x:int = 0
    self.scroll_y:int = 0
    self.scroll_dx:int = 0
    self.scroll_dy:int = 0

    # initialize maze
    self.maze = [ 1 ] * self.width * self.height
    self.dig_positions = []

  def push(self, pos):
    self.dig_positions.append(pos)
  
  def pop(self):
    if not self.dig_positions:
      return None
    else:
      return self.dig_positions.pop()

  def scroll(self, arg):
    self.scroll_x = (self.scroll_x + self.scroll_dx + 1024) % 1024
    self.scroll_y = (self.scroll_y + self.scroll_dy + 1024) % 1024
    self.g.home(self.scroll_x, self.scroll_y)

  def dig(self, pos):

    # dig position
    (x, y) = pos

    # possible digging directions
    ds = []       
    if y > 1 and self.maze[ (y - 1) * self.width + x ] and self.maze[ (y - 2) * self.width + x ]:
      ds.append(0)
    if x > 1 and self.maze[ y * self.width + x - 1 ] and self.maze[ y * self.width + x - 2 ]:
      ds.append(1)
    if y < self.height - 2 and self.maze[ (y + 1) * self.width + x ] and self.maze[ (y + 2) * self.width + x ]:
      ds.append(2)
    if x < self.width - 2 and self.maze[ y * self.width + x + 1 ] and self.maze[ y * self.width + x + 2 ]:
      ds.append(3)

    # no more direction
    if not ds:
      return None

    # dig
    d = random.choice(ds)
    if d == 0:    # up
      self.maze[ (y - 1) * self.width + x ] = 0
      self.maze[ (y - 2) * self.width + x ] = 0
      if self.g:
        self.g.fill( 8 + x * 16, 8 + (y - 2) * 16, 8 + x * 16 + 15, 8 + (y - 1) * 16 + 15, 0)
      y -= 2
    elif d == 1:  # left
      self.maze[ y * self.width + x - 1 ] = 0
      self.maze[ y * self.width + x - 2 ] = 0
      if self.g:
        self.g.fill( 8 + (x - 2) * 16, 8 + y * 16, 8 + (x - 1) * 16 + 15, 8 + y * 16 + 15, 0)
      x -= 2
    elif d == 2:  # down
      self.maze[ (y + 1) * self.width + x ] = 0
      self.maze[ (y + 2) * self.width + x ] = 0
      if self.g:
        self.g.fill( 8 + x * 16, 8 + (y + 1) * 16, 8 + x * 16 + 15, 8 + (y + 2) * 16 + 15, 0)
      y += 2
    elif d == 3:  # right
      self.maze[ y * self.width + x + 1 ] = 0
      self.maze[ y * self.width + x + 2 ] = 0
      if self.g:
        self.g.fill( 8 + (x + 1) * 16, 8 + y * 16, 8 + (x + 2) * 16 + 15, 8 + y * 16 + 15, 0)
      x += 2

    # return new dig position
    self.pos = (x, y)

    return self.pos


# main
def main():

  # randomize
  random.seed(int(time.time() * 10))

  # initialize screen
  x68k.crtmod(16, True)
  x68k.curoff()
  x68k.iocs(x68k.i.TXFILL,a1=pack('6h',0,0,0,1024,1024,0))
  x68k.iocs(x68k.i.TXFILL,a1=pack('6h',1,0,0,1024,1024,0))
  g = x68k.GVRam(0)
  g.window(0, 0, 1023, 1023)
  g.fill(0, 0, 1023, 1023, 0)
  x68k.vpage(1)
  
  # scroll direction patterns
  dx = [ 1, 0, -1,  0, 1,  1, -1, -1 ]
  dy = [ 0, 1,  0, -1, 1, -1,  1, -1 ]

  pos = None

  # main loop up to 16 times
  for i in range(16):

    # initialize graphic page
    g.fill(0, 0, 1023, 1023, random.randrange(2, 14, 2))
    g.home(0, 0)

    # initialize maze
    m = Maze(MAZE_WIDTH, MAZE_HEIGHT, g)
    m.scroll_dx = dx[ i % 8 ]
    m.scroll_dy = dy[ i % 8 ]

    # select initial digging position
    x0 = random.randrange(1, MAZE_WIDTH  - 2, 2)     # initial X
    y0 = random.randrange(1, MAZE_HEIGHT - 2, 2)     # initial Y
    pos = (x0, y0)
    m.push(pos)

    with x68k.Super(), x68k.IntVSync(m.scroll, m):
 
      # dig
      while True:

        # check shift key to exit
        if x68k.iocs(x68k.i.B_SFTSNS) & 0x01:
          i = 999
          break

        # dig ops
        next_pos = m.dig(pos)  # dig and get the next position
        if next_pos is not None:            # if next position is available  
          pos = next_pos                    # continue to dig
          m.push(pos)                       # remember as future potential dig position
        else:                               # if we cannot dig with the current position, back to previous positions
          pos = m.pop()                     # pop from the candidate position list
          if pos is None:                   # if no more dig position
            break                           # digging complete

      # abort check
      if i >= 999:
        break

      # maze complete
      x68k.vsync()
      g.home(0, 0)
      time.sleep(3)

  # cursor on
  x68k.curon()

# run
if __name__ == "__main__":
  main()