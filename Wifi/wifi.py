def converInHex(str):
  return ":".join("{:02x}".format(ord(c)) for c in str)

cmd = 'C'
di = 'L'
servo0 = 50
servo1 = 60
servo2 = 70
servo3 = 80
packetCount = 255

# packet size = 1+1+4+4 = 10 byte
from struct import pack
# Check the range
pac = cmd + di + pack('BBBBI', servo0, servo1, servo2, servo3, packetCount)
print converInHex(pac)
