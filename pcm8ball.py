import x68k
import machine
import uctypes
import random
import time
from struct import pack

class PCM8:

  def is_available(self):
    eye_catch = []
    eye_catch_addr = x68k.iocs(x68k.i.B_LPEEK,a1=0x0088)
    for i in range(8):
      eye_catch.append(x68k.iocs(x68k.i.B_BPEEK,a1=(eye_catch_addr + i - 8)))
    return bytes(eye_catch) == 'PCM8/048'.encode()

class SpritePattern:

  def clear(self):
    x68k.iocs(x68k.i.SP_INIT)
    for i in range(256):
      x68k.iocs(x68k.i.SP_CGCLR,d1=i)
    x68k.iocs(x68k.i.SP_ON)   

  def define_pattern(self, code, size, pattern):
    x68k.iocs(x68k.i.SP_DEFCG,d1=0,d2=0,a1=uctypes.addressof(bytes(sp_pat_star)))

pcm8 = PCM8()
if pcm8.is_available() != True:
  print("pcm8 is not running.")
else:
  print("pcm8 is running.")