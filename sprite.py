import x68k
import machine
import uctypes
from random import randint

REG_SP_SCROLL  = const(0xEB0000)
REG_SP_PALETTE = const(0xE82200)
REG_GPIP       = const(0xE88001)

NUM_STARS = 32
STAR_SPEED = 40

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

# main loop
while True:

  # check shift key to exit
  if x68k.iocs(x68k.i.B_SFTSNS):
    break

  # move stars
  for i in range(NUM_STARS):
    star_z[i] -= STAR_SPEED
    if star_z[i] < 0:
      star_z[i] += 2048
    w = 512.0 + (2048.0-512.0)*(star_z[i]/2048.0)
    s = 512.0/w
    star_x2[i] = int(star_x[i] * s) + 256
    star_y2[i] = int(star_y[i] * s) + 256

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

x68k.iocs(x68k.i.OS_CURON)
