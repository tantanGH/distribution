import x68k
import time

x68k.crtmod(16,True)
time.sleep(1)

# direct cursor addressing + highlight
print("\x1b[8;10H" + "\x1b[1m" + "Hello, uPython at (10,8).", end="")
time.sleep(1)

# direct cursor addressing + reverse
print("\x1b[15;20H" + "\x1b[7m" + "Hello, uPython at (20,15).", end="")
time.sleep(1)

# cursor up + cyan
print("\x1b[1A" + "\x1b[31m" + "Cursor up!", end="")
time.sleep(1)

# cursor down + yellow
print("\x1b[2B" + "\x1b[32m" + "Cursor down!", end="")
time.sleep(1)

# cursor backward + bold cyan
print("\x1b[50D" + "\x1b[35m" + "Cursor backward!", end="")
time.sleep(1)

# cursor forward + bold yellow
print("\x1b[40C" + "\x1b[36m" + "Cursor forward!", end="")
time.sleep(1)

# direct cursor addressing + reverse highlight cyan
print("\x1b[12;0H" + "\x1b[45m" + "Jump here.", end="")
time.sleep(1)

# reset + clear from cursor to end of screen + reversed highlight yellow
print("\x1b[m" + "\x1b[0J" + "\x1b[46m" + "Cleared here to end of screen!", end="")
time.sleep(1)

# reset + clear screen
print("\x1b[m" + "\x1b[2J" + "All clear and back to home!", end="")
time.sleep(1)
