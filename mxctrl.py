import x68k
import uctypes
import machine
import time
from uctypes import addressof
from struct import pack

# MXDRV class
class MXDRV:

  # constructor
  def __init__(self):
    eye_catch_addr = x68k.iocs(x68k.i.B_LPEEK,a1=0x0090)    # trap 4 vector
    eye_catch = []
    for i in range(12):
      eye_catch.append(x68k.iocs(x68k.i.B_BPEEK,a1=(eye_catch_addr + i - 12)))
    if bytes(eye_catch) != b'EX16mxdrv206':
      raise RuntimeError("MXDRV is not running.")

  # $02 LOADMML
  @micropython.asm_m68k
  def loadpcm_asm(self, mml, mml_len):
    movel(0x02,d0)
    movel([16,fp],d1)
    movel([12,fp],a1)
    trap(4)

  def loadmml(self, mml_name, mml_data, use_pdx):
    mml = bytearray([0,0, 0 if use_pdx else 0xff, 0 if use_pdx else 0xff, 0,270, 0,8])
    mml.extend(mml_name.decode())
    mml.extend(bytes([0] * len(p)-270))
    mml.extend(mml_data)
    loadmml_asm(self,mml,len(mml))
	
  # $03 LOADPCM
  @micropython.asm_m68k
  def loadpcm_asm(self, pcm, pcm_len):
    movel(0x03,d0)
    movel([16,fp],d1)
    movel([12,fp],a1)
    trap(4)

  def loadpcm(self, pcm_name, pcm_data):
    pcm = bytearray([0,0, 0,0, 0,270, 0,8])
    pcm.extend(pcm_name.decode())
    pcm.extend(bytes([0] * len(p)-270))
    pcm.extend(pcm_data)
    loadpcm_asm(self,pcm,len(pcm))
	
  # $04 M_PLAY
  @micropython.asm_m68k
  def m_play(self):
    movel(0x04,d0)
    trap(4)

  # $05 M_END
  @micropython.asm_m68k
  def m_end(self):
    movel(0x05,d0)
    trap(4)

  # $06 M_STOP
  @micropython.asm_m68k
  def m_stop(self):
    movel(0x06,d0)
    trap(4)

  # $07 M_CONT
  @micropython.asm_m68k
  def m_cont(self):
    movel(0x07,d0)
    trap(4)

  # $08 MMLNAME
  @micropython.asm_m68k
  def mmlname_asm(self):
    movel(0x08,d0)
    movel(0,d1)
    trap(4)

  def mmlname(self):
    addr = self.mmlname_asm()
    name = bytearray()
    while True:
      c = machine.mem8[ addr ]
      if c == 0:
        break
      name.append(c)
      addr += 1
    return bytes(name)

  # $09 PCMNAME
  @micropython.asm_m68k
  def pcmname_asm(self):
    movel(0x09,d0)
    movel(0,d1)
    trap(4)

  def pcmname(self):
    addr = self.pcmname_asm()
    name = bytearray()
    while True:
      c = machine.mem8[ addr ]
      if c == 0:
        break
      name.append(c)
      addr += 1
    return bytes(name)

  # $0C M_FADEOUT
  @micropython.asm_m68k
  def m_fadeout(self, speed=12):
    movel(0x0c,d0)
    movel([12,fp],d1)
    trap(4)

  # $12 M_STAT
  @micropython.asm_m68k
  def m_stat(self):
    movel(0x12,d0)
    trap(4)

# main
def main():

  # MXDRV object
  mxdrv = MXDRV()

  # stop current play
  mxdrv.m_stop()

  # load MDX

  # load PDX

  # start play
  mxdrv.m_play()

  # playing title
  print("MXDRV is now playing [", end="")
  x68k.dos(x68k.d.PRINT,pack('l',addressof(mxdrv.mmlname())))
  print("]")

  # sleep
  time.sleep(3)

  # fadeout
  mxdrv.m_fadeout(12)

if __name__ == "__main__":
  main()
