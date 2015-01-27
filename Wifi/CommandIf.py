import sys, os
from struct import pack
import select
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox


parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from Wifi.SocketIf import SocketIf
import Model.Constant as Constant
from Model.CommonFunction import converInHex



class CommandIf(SocketIf):
  """docstring for CommandIf"""
  def __init__(self, host, port):
    SocketIf.__init__(self, host, port)
    
    self.rxPacketCount = 0
    self.txPacketCount = 0

    self.buffersize = Constant.DATABUFFERSIZE
    self.msgPip = []

    self.updateStatus = False

  def __str__(self):
    ret = "Target Address:"  + str(self.client_Address)
    ret +=  "Connected: %s " % Data.serverConnection
    ret += "Rx Packets: %d " % self.rxPacketCount
    ret += "Tx Packets: %d " % self.txPacketCount
    return ret

  def sendStartCmd(self):
    # Send command to start control leap
    return True

  def update(self, dataList):
    self.updateStatus = True
    self.dataList = dataList

  def sendNewUpdate(self, _msg = ''):
    cmd = 'C'

    # di = 0
    # servo0 = 50
    # servo1 = 60
    # servo2 = 70
    # servo3 = 80
    # speed = -15

    speed = self.dataList[0]
    di = self.dataList[1]
    servo0 = self.dataList[2]
    servo1 = self.dataList[3]
    servo2 = self.dataList[4]
    servo3 = self.dataList[5]



    packetCount = 255
    length = 15

    print 'sending'

    pac = pack('cBBBBBBiI', cmd, length, di, servo0, servo1, servo2, servo3, speed, packetCount)
    pac += 'end'
    length = len(pac)
    pac = pac[0] + pack('B', length) + pac[2:]

    self.sock.sendto(pac, self.addr)
    packetCount +=1



  def run(self):

    print "Start wifi connection"

    UPD_IP = ''
    UPD_PORT = 55555

    data = self.receiveMsg()
    print "receive: " + data

    while 1:
      self.sock.setblocking(0)
      hasData = select.select([self.sock], [], [], 0.5)
      if hasData[0]:
        data = self.sock.recvfrom(self.buffersize)
        print data[0]
      else:
        if self.updateStatus == True:
          self.updateStatus = False
          self.sendNewUpdate()



if __name__ == '__main__':
  app = QApplication(sys.argv)

  command_if_thread = CommandIf('', 55555)
  command_if_thread.start()

  sys.exit(app.exec_())
  print "hi"
