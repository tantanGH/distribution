import x68k
import uctypes

voice_set = {

  # @1 brass#1
  1: [
    #  AF   SM   WF   SY   SP  PMD  AMD  PMS  AMS  PAN  RSV
    7*8+5,  15,   0,   0,   0,   0,   0,   0,   0,   3,   0,
    #  AR  D1R  D2R   RR  D1L   TL   KS  MUL  DT1  DT2  AME
       13,  31,  11,   7,   0,  29,   0,   1,   0,   0,   0 ,
       16,  31,   0,   9,   0,   8,   0,   1,   0,   0,   0 ,
       14,  31,   0,   8,   0,  27,   0,   1,   3,   0,   0 ,
       15,  31,   0,   8,   0,   8,   0,   1,   3,   0,   0 ,
  ],

  # @2 brass#2
  2: [
    #  AF   SM   WF   SY   SP  PMD  AMD  PMS  AMS  PAN  RSV
    7*8+2,  15,   0,   0,   0,   0,   0,   0,   0,   3,   0,
    #  AR  D1R  D2R   RR  D1L   TL   KS  MUL  DT1  DT2  AME
       16,   7,   7,   6,   5,  28,   0,   1,   0,   0,   0 ,
       31,  19,   0,   9,  15,  12,   0,   2,   0,   1,   0 ,
       14,  12,   0,   9,   5,  33,   0,   1,   0,   0,   0 ,
       20,  31,   0,   9,   0,   7,   0,   1,   0,   0,   0 ,
  ],

}

mml_set = {

  # track 1 MML
  1: """
t90
@1q5l8v15o4
e.e16eddd cdefed efga<c>a gfed.d16d e.e16eece d2.
""",

  # track 2 MML
  2: """
@2q5l8v15o4
c.c16c>ggg eg<cdc>g< cdefaf edc>g.g16g< c.c16cc>e<c> g2.
""",

}

# _M_INIT
x68k.iocs(x68k.i.OPMDRV,d1=0)

# _M_VSET
for vnum,vdata in voice_set.items():
  x68k.iocs(x68k.i.OPMDRV,d1=4,d2=vnum,a1=uctypes.addressof(bytes(vdata)))

# _M_ALLOC & _M_ASSIGN
for trk in mml_set:
  ch = trk
  x68k.iocs(x68k.i.OPMDRV,d1=1,d2=(trk << 16)|1024)     # trk buffer 1024 bytes
  x68k.iocs(x68k.i.OPMDRV,d1=2,d2=(ch << 16)|trk)       # opm ch = trk

# _M_TRK
for trk,mml in mml_set.items():
  x68k.iocs(x68k.i.OPMDRV,d1=6,d2=trk,a1=uctypes.addressof(mml.replace('\r','').replace('\n','')+"\x00"))

# _M_PLAY
x68k.iocs(x68k.i.OPMDRV,d1=8,d2=0)
