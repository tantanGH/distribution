import os

# 9600bps / 8bit / Parity none / Stop 1bit / No flow control
os.system("SPEED.X 9600 B8 PN S1 NONE")

with open("AUX","r+") as uart:

#  uart.write("Hello, I am from MicroPython on X68000Z\n")
  uart.write("‚±‚ñ‚É‚¿‚Í\n")

  print(uart.readline(), end="")
  
  uart.write("Thank you!\n")