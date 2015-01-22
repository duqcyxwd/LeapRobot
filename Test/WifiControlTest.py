from struct import pack
import socket
import select
import sys
from time import sleep, time

def converInHex(str):
  return ":".join("{:02x}".format(ord(c)) for c in str)
 
cmd = 'C'
di = 0
servo0 = 50
servo1 = 60
servo2 = 70
servo3 = 80
speed = -15
packetCount = 255

 
UPD_IP = ''
UPD_PORT = 55555
BUFFER_SIZE = 1024
 
print 'Start connection'
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((UPD_IP, UPD_PORT))
 
data, addr = soc.recvfrom(BUFFER_SIZE)
print "receive: " + data
print addr
 
length = 15
t= time()
while 1:
 
    soc.setblocking(0)
    hasData = select.select([soc], [], [], 0.5)
    if hasData[0]:
        data = soc.recvfrom(BUFFER_SIZE)
        print data[0]
    else:
        print 'sending'
        pac = pack('cBBBBBBiI', cmd, length, di, servo0, servo1, servo2, servo3, speed, packetCount)
        pac += 'end'
        length = len(pac)
        pac = pac[0] + pack('B', length) + pac[2:]
 
        soc.sendto(pac, addr)
        packetCount +=1

    t2= time()
    if (t2 - t) > 30:
      print "send new command"
      pass

