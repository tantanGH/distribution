import x68k
import machine
import uctypes
import random
import time
from struct import pack

REG_SP_SCROLL  = const(0xEB0000)

NUM_STARS = 32

STAR_SPEED_MAX = 128
STAR_SPEED_MIN = 40

# randomize
random.seed(int(time.time() * 10))

# initialize screen
x68k.crtmod(12,True)
x68k.curoff()
x68k.iocs(x68k.i.TXFILL,a1=pack('6h',0,0,0,1024,1024,0))
x68k.iocs(x68k.i.TXFILL,a1=pack('6h',1,0,0,1024,1024,0))

# supervisor mode
s = x68k.super()

# reset sprite
x68k.iocs(x68k.i.SP_INIT)
for i in range(256):
  x68k.iocs(x68k.i.SP_CGCLR,d1=i)
x68k.iocs(x68k.i.SP_ON)

# set sprite pattern
sp_pat_star = [ 0x11, 0x10, 0x00, 0x00, 0x11, 0x10, 0x00, 0x00,
                0x11, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ]
x68k.iocs(x68k.i.SP_DEFCG,d1=0,d2=0,a1=uctypes.addressof(bytes(sp_pat_star)))

# set sprite palette
x68k.iocs(x68k.i.SPALET,d1=pack('L',(1<<31)|1),d2=1,d3=0b11111_11111_11111_1)
x68k.iocs(x68k.i.SPALET,d1=pack('L',(1<<31)|1),d2=2,d3=0b01000_10000_00110_1)
x68k.iocs(x68k.i.SPALET,d1=pack('L',(1<<31)|1),d2=3,d3=0b10001_10001_10001_1)

# initialize 3D star positions
star_x = []
star_y = []
star_z = []
for i in range(NUM_STARS):
  star_x.append(random.randint(0,2047)-1024)
  star_y.append(random.randint(0,2047)-1024)
  star_z.append(random.randint(0,2047))

# initialize 2D star positions
star_x2 = [0] * NUM_STARS
star_y2 = [0] * NUM_STARS

# initialize star speed
star_speed_x = 0
star_speed_y = 0
star_speed_z = STAR_SPEED_MIN

# main loop
while True:

  # check shift key to exit
  if x68k.iocs(x68k.i.B_SFTSNS) & 0x01:
    break

  # check joystick left/right for X move
  joy = x68k.iocs(x68k.i.JOYGET,d1=0)
  if (joy & 0x08) == 0:    # right
    star_speed_x = -12
  elif (joy & 0x04) == 0:  # left
    star_speed_x = 12
  else:
    star_speed_x = 0

  # check joystick up/down for Y move
  if (joy & 0x02) == 0:     # down
    star_speed_y = -8
  elif (joy & 0x01) == 0:   # up
    star_speed_y = 8
  else:
    star_speed_y = 0

  # check joystick B button for Z acceleration
  if (joy & 0x40) == 0:     # button B
    if star_speed_z < STAR_SPEED_MAX:
      star_speed_z += 1
  else:
    if star_speed_z > STAR_SPEED_MIN:
      star_speed_z -= 3

  # move stars
  for i in range(NUM_STARS):

    if star_speed_x != 0:
      star_x[i] += star_speed_x
      if star_x[i] < -1024:
        star_x[i] += 2048
      elif star_x[i] > 1024:
        star_x[i] -= 2048

    if star_speed_y != 0:
      star_y[i] += star_speed_y
      if star_y[i] < -1024:
        star_y[i] += 2048
      elif star_y[i] > 1024:
        star_y[i] -= 2048

    star_z[i] -= star_speed_z
    if star_z[i] < 0:
      star_z[i] += 2048

    w = 512.0 + (2048.0 - 512.0)*(float(star_z[i])/2048.0)
    s = 512.0/w

    star_x2[i] = int(star_x[i] * s) + 256
    star_y2[i] = int(star_y[i] * s) + 256

  # scroll stars
  x68k.vsync()
  for i in range(NUM_STARS):
    if star_x2[i] >= 0 and star_x2[i] < 512 and star_y2[i] >= 0 and star_y2[i] < 512:
      machine.mem16[ REG_SP_SCROLL + i * 8 + 0 ] = 16 + star_x2[i]
      machine.mem16[ REG_SP_SCROLL + i * 8 + 2 ] = 16 + star_y2[i]
      machine.mem16[ REG_SP_SCROLL + i * 8 + 4 ] = ((1 + i%3) << 8) | 0
      machine.mem16[ REG_SP_SCROLL + i * 8 + 6 ] = 3    
    else:
      machine.mem16[ REG_SP_SCROLL + i * 8 + 6 ] = 0

# user mode
x68k.super(s)

# cursor on
x68k.curon()