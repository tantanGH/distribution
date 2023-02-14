import x68k
import uctypes

# opmdrv class
class OPMDRV:

  # constructor
  def __init__(self):
    opmdrv_vector = x68k.iocs(x68k.i.B_LPEEK,a1=(0x000400 + 4 * 0xf0))  # check IOCS $F0 vector
    if opmdrv_vector < 0:
      raise RuntimeError("OPMDRV is not installed.")

  # _M_INIT
  def m_init(self):    
    x68k.iocs(x68k.i.OPMDRV,d1=0)   

  # _M_ALLOC
  def m_alloc(self, trk, size):
    x68k.iocs(x68k.i.OPMDRV,d1=1,d2=(trk << 16)|size)

  # _M_ASSIGN
  def m_assign(self, ch, trk):
    x68k.iocs(x68k.i.OPMDRV,d1=2,d2=(ch << 16)|trk)

  # _M_VSET
  def m_vset(self, vnum, vdata):
    x68k.iocs(x68k.i.OPMDRV,d1=4,d2=vnum,a1=uctypes.addressof(bytes(vdata)))

  # _M_TEMPO
  def m_tempo(self, tempo):
    x68k.iocs(x68k.i.OPMDRV,d1=5,d2=tempo)

  # _M_TRK
  def m_trk(self, trk, mml):
    x68k.iocs(x68k.i.OPMDRV,d1=6,d2=trk,a1=uctypes.addressof(mml.replace('\r','').replace('\n','')))

  # _M_PLAY
  def m_play(self, trk=0):
    x68k.iocs(x68k.i.OPMDRV,d1=8,d2=trk)

  # _M_STOP
  def m_stop(self, trk=0):
    x68k.iocs(x68k.i.OPMDRV,d1=10,d2=trk)

# main
def main():

  # custom voices
  voices = {

    1: [
      #  AF   SM   WF   SY   SP  PMD  AMD  PMS  AMS  PAN  RSV
      7*8+2,  15,   0,   0,   0,   0,   0,   0,   0,   3,   0,
      #  AR  D1R  D2R   RR  D1L   TL   KS  MUL  DT1  DT2  AME
         31,   0,   0,   0,   0,  27,   0,   2,   0,   0,   0,
         31,   0,   0,   0,   0,  62,   0,   2,   0,   0,   0,
         31,   0,   0,   0,   0,  46,   0,   1,   0,   0,   0,
         31,  13,   0,  13,  15,   0,   0,   1,   0,   0,   0,
    ],

  }

  # MML
  mmls = {

    # track 1 MML
    1: """
@1q7l8v15o5
c+2&c+8d2e4. d2&d8c+2d4. a1&a2 b4a8g4f+4.e8d4.
""",

    # track 2 MML
    2: """
@1q7l8v14o4
a2&a8b2<c+4.> b2&b8a2b4. <c+2&c+8d2e4. d2&d8>b2.. 
""",

    # track 3 MML
    3: """
@1q4l8v15o3
g4d8g4d8g4d8g4d8 g4d8g4d8g4d8g4d8 f+4c+8f+4c+8f+4c+8f+4c+8 >b4.<c+4d4.e8f+4.
  """,

  }

  # opmdrv instance
  opmdrv = OPMDRV()
  
  # opmdrv init
  opmdrv.m_init()

  # track buffer allocation and channel assignment
  for t in mmls:
    ch = t
    opmdrv.m_alloc(t, 1024)
    opmdrv.m_assign(ch, t)

  # setup custom voice data
  for vnum,vdata in voices.items():
    opmdrv.m_vset(vnum, vdata)

  # setup mml
  for trk,mml in mmls.items():
    opmdrv.m_trk(trk, mml)
  
  # setup tempo
  opmdrv.m_tempo(220)

  # play
  opmdrv.m_play()


if __name__ == "__main__":
  main()
