import x68k
import random
import time
from uctypes import addressof
from struct import pack

# randomize
random.seed(int(time.time() * 10))

# score
score = 0

# initial snake pos
snake_x = 32
snake_y = 24

# block lines frame buffer for collision check
block_lines = [ " " * 64 ] * (snake_y - 1)

# function key display off
funckey_mode = x68k.dos(x68k.d.CONCTRL,pack('hh',14,3))

# screen mode
x68k.crtmod(12,True)

# cursor off
x68k.curoff()

# print snake
for y in range(snake_y,32):
  s = f"\x1b[{y};{snake_x}H" + "\x1b[37m" + "S"
  x68k.dos(x68k.d.CONCTRL,pack('hl',1,addressof(s)))

while True:

  # check left and right keys 
  scan_code = x68k.dos(x68k.d.KEYCTRL,pack('hh',3,7))
  if scan_code & 0x08:      # left key
    if snake_x > 1:
      snake_x -= 1
  elif scan_code & 0x20:    # right key
    if snake_x < 64:
      snake_x += 1

  # new road blocks line
  block_line = " " * 64
  bx1 = random.randint(0,99)
  if bx1 >= 1 and bx1 <= 62:
    block_line = block_line[:bx1-1] + "***" + block_line[bx1-1+3:]
  bx2 = random.randint(0,199)
  if bx2 >= 1 and bx2 <= 59:
    block_line = block_line[:bx2-1] + "******" + block_line[bx2-1+6:]
  block_lines.append(block_line)

  # vsync wait
  x68k.vsync()

  # scroll down
  x68k.dos(x68k.d.CONCTRL,pack('hhh',3,0,0))
  x68k.dos(x68k.d.CONCTRL,pack('h',5))

  # print block line
  s = f"\x1b[0;0H" +  "\x1b[32m" + block_line
  x68k.dos(x68k.d.CONCTRL,pack('hl',1,addressof(s)))    

  # collision check
  check_line = block_lines.pop(0)
  if (check_line[snake_x-1] == '*'):
    s = "\x1b[14;24H" + "\x1b[46m" + "    OUCH!!!!    "
    x68k.dos(x68k.d.CONCTRL,pack('hl',1,addressof(s)))
    break

  # snake head
  s = f"\x1b[{snake_y};{snake_x}H" + "\x1b[37m" + "S"
  x68k.dos(x68k.d.CONCTRL,pack('hl',1,addressof(s)))

  # increment score
  score += 100

# display score
s = "\n\x1b[16;24H" + "\x1b[35m" + "YOUR SCORE: " + "\x1b[37m" + f"{score}" + "\x1b[m\n"
x68k.dos(x68k.d.CONCTRL,pack('hl',1,addressof(s)))

# flush key buffer
x68k.dos(x68k.d.KFLUSH,pack('h',0))  

# resume function key display mode
x68k.dos(x68k.d.CONCTRL,pack('hh',14,funckey_mode))

# cursor on
x68k.curon()
