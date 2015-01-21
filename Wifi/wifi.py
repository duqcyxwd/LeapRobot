def converInHex(str):
  return ":".join("{:02x}".format(ord(c)) for c in str)



# packet size = 1+1+4+4 = 10 byte
# Check the range



#!/usr/bin/env python
import socket
import select
import sys
from time import sleep 

# UPD_IP = 'Localhost' # check the 255.255.255 later. 
# UPD_IP = '255.255.255' # check the 255.255.255 later. 
# UPD_IP = '192.168.0.100'

