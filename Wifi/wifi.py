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

# packet size = 1+1+4+4 = 10 byte
from struct import pack
# Check the range



#!/usr/bin/env python
import socket
import select
import sys
from time import sleep 

# UPD_IP = 'localhost' # check the 255.255.255 later. 
# UPD_IP = '255.255.255' # check the 255.255.255 later. 
UPD_IP = '192.168.0.103'
UPD_PORT = 55555
BUFFER_SIZE = 1024

print 'Start connection'
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind((UPD_IP, UPD_PORT))

data, addr = soc.recvfrom(BUFFER_SIZE)
print "receive: " + data
print addr

i = 0
length = 15

while 1:

	soc.setblocking(0)
	hasData = select.select([soc], [], [], 0.5)
	if hasData[0]:
		data = soc.recvfrom(BUFFER_SIZE)
		print data[0]
	else:
		# sleep(1)
		# print "send CL" %i
		# s.sendto("%d" % i, addr)
		# s.sendto("abcd%i"%4, addr)
		print 'sending'
		pac = pack('cBBBBBBiI', cmd, length, di, servo0, servo1, servo2, servo3, speed, packetCount)
		pac += 'end'
		length = len(pac)
		pac = pac[0] + pack('B', length) + pac[2:]

		soc.sendto(pac, addr)

		# print converInHex(pac)
		# print len(pac)
		i += 1
		# i %=10
		packetCount +=1
