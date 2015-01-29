import socket
import os
import select

from PyQt5 import QtCore

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import Model.Constant as Constant

# UDP Connection
# Socket Connection inter face
class SocketIf(QtCore.QThread):
  """docstring for SocketIf"""
  def __init__(self, _host, _port):
    QtCore.QThread.__init__(self)

    self.targetAddress = (_host, _port)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(self.targetAddress)
    # self.sock.listen(5)


    self.packetCounter = 0
    self.conn = 0
    self.addr = 0

    self.buffersize = Constant.DATABUFFERSIZE
    self.receiveTimeout = Constant.RECEIVE_TIMEOUT

  def __str__(self):
    return "Connection to:"  + str(self.targetAddress)

  def buildConnection(self):
    try:
      print "Building connection"
      print "Waiting for Client connect from " + str(self.targetAddress)
      self.conn, self.addr = self.sock.accept()
      print 'Got connection from:' + str(self.addr)
      return True
    except:
      return False

  # Return empty if there is no message
  def receiveMsg(self):
    self.sock.setblocking(0)
    hasData = select.select([self.sock], [], [], self.receiveTimeout)
    if hasData[0]:
      data, addr = self.sock.recvfrom(self.buffersize)
      self.addr = addr
      return data[0]
    return  ""

  def sendMsg(self, mes):
    self.sock.sendto(mes, self.addr)

  def closeSocket(self):
    self.sock.close()
    print "Socket closed"
    # self.connected = False
