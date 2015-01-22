from struct import pack
import socket
import select
import sys
from time import sleep, time

def converInHex(str):
  return ":".join("{:02x}".format(ord(c)) for c in str)
 
cmd = 'C'
di = 1
servo0 = 65  # Base
servo1 = 65  # 
servo2 = 75
servo3 = 25
speed = -150

packetCount = 250
 
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
    sleep(2)
    soc.setblocking(0)
    hasData = select.select([soc], [], [], 0.5)
    if hasData[0]:
        data = soc.recvfrom(BUFFER_SIZE)
        print data[0]
    else:
        print 'sending' + str(di)
        pac = pack('cBBBBBBiI', cmd, length, di, servo0, servo1, servo2, servo3, speed, packetCount)
        pac += 'end'
        length = len(pac)
        pac = pac[0] + pack('B', length) + pac[2:]
        soc.sendto(pac, addr)
        packetCount +=1

    t2= time()
    if (t2 - t) > 20:
        print "send new command"
        # if speed > - 150 :
        #     speed -= 10
        # elif speed < 150:
        #     speed += 4

        speed = speed * -1

        di = (di + 1)%3
