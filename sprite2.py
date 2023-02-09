import x68k
import machine
import uctypes
from random import randint

REG_SP_SCROLL  = const(0xEB0000)
REG_SP_PALETTE = const(0xE82200)
REG_GPIP       = const(0xE88001)

NUM_STARS = 32

SHIP_SPEED_MAX = 128
SHIP_SPEED_MIN = 40

# initialize screen
x68k.crtmod(12,True)
x68k.iocs(x68k.i.B_SUPER,a1=0)
x68k.iocs(x68k.i.G_CLR_ON)
x68k.iocs(x68k.i.OS_CUROF)

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
machine.mem16[ REG_SP_PALETTE + 1 * 16 * 2 + 1 * 2 ] = 0b11111_11111_11111_1
machine.mem16[ REG_SP_PALETTE + 2 * 16 * 2 + 1 * 2 ] = 0b01000_10000_00110_1
machine.mem16[ REG_SP_PALETTE + 3 * 16 * 2 + 1 * 2 ] = 0b10001_10001_10001_1

# initialize 3D star positions
star_x = []
star_y = []
star_z = []
for i in range(NUM_STARS):
  star_x.append(randint(0,2047)-1024)
  star_y.append(randint(0,2047)-1024)
  star_z.append(randint(0,2047))

# initialize 2D star positions
star_x2 = [0] * NUM_STARS
star_y2 = [0] * NUM_STARS

# initialize 3D ship position and speed
ship_x = 0
ship_y = 0
ship_z = 0
ship_speed_z = SHIP_SPEED_MIN

# main loop
while True:

  # check shift key to exit
  if x68k.iocs(x68k.i.B_SFTSNS):
    break

  # check joystick left/right for ship X move
  joy = x68k.iocs(x68k.i.JOYGET,d1=0)
  if (joy & 0x04) == 0:    # left
    ship_x -= 12
    if ship_x < -1024:
      ship_x += 2048
  elif (joy & 0x08) == 0:  # right
    ship_x += 12
    if ship_x > 1024:
      ship_x -= 2048

  # check joystick up/down for ship Y move
  if (joy & 0x01) == 0:     # up
    ship_y -= 8
    if ship_y < -1024:
      ship_y += 2048
  elif (joy & 0x02) == 0:   # down
    ship_y += 8
    if ship_y > 1024:
      ship_y -= 2048

  # check joystick B button for ship Z acceleration
  if (joy & 0x40) == 0:     # button B
    if ship_speed_z < SHIP_SPEED_MAX:
      ship_speed_z += 1
  else:
    if ship_speed_z > SHIP_SPEED_MIN:
      ship_speed_z -= 3

  # move ship Z positions
  ship_z += ship_speed_z
  if ship_z > 2048:
    ship_z -= 2048

  # map stars to 2D positions
  for i in range(NUM_STARS):

    rx = star_x[i] - ship_x
    if rx < -1024:
      rx += 2048
    elif rx > 1024:
      rx -= 2048

    ry = star_y[i] - ship_y
    if ry < -1024:
      ry += 2048
    elif ry > 1024:
      ry -= 2048

    rz = star_z[i] - ship_z
    if rz < 0:
      rz += 2048

    w = 512.0 + (2048.0 - 512.0)*(float(rz)/2048.0)
    s = 512.0/w

    star_x2[i] = int(rx * s) + 256
    star_y2[i] = int(ry * s) + 256

  # wait vblank
  while (machine.mem8[ REG_GPIP ] & 0x10) == 0:
    pass
  while (machine.mem8[ REG_GPIP ] & 0x10) != 0:
    pass

  # scroll stars
  for i in range(NUM_STARS):
    if star_x2[i] >= 0 and star_x2[i] < 512 and star_y2[i] >= 0 and star_y2[i] < 512:
      machine.mem16[ REG_SP_SCROLL + i * 8 + 0 ] = 16 + star_x2[i]
      machine.mem16[ REG_SP_SCROLL + i * 8 + 2 ] = 16 + star_y2[i]
      machine.mem16[ REG_SP_SCROLL + i * 8 + 4 ] = ((1 + i%3) << 8) | 0
      machine.mem16[ REG_SP_SCROLL + i * 8 + 6 ] = 3    
    else:
      machine.mem16[ REG_SP_SCROLL + i * 8 + 6 ] = 0

# cursor on
x68k.iocs(x68k.i.OS_CURON)