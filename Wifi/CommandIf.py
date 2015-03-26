import sys, os
from struct import pack
import select
from time import sleep, time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from Wifi.SocketIf import SocketIf
import Model.Constant as Constant
from Model.CommonFunction import converInHex

import logging

import logging

formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)-3d]:  %(message)s')

outLogger = logging.getLogger("outLogger");
logf = logging.FileHandler("out.log")
logf.setFormatter(formatter)
outLogger.addHandler(logf)
outLogger.setLevel(logging.INFO)


inLogger = logging.getLogger("inLogger");
logf2 = logging.FileHandler("in.log")
logf2.setFormatter(formatter)
inLogger.addHandler(logf2)
inLogger.setLevel(logging.INFO)

class CommandIf(SocketIf):
  """docstring for CommandIf"""
  def __init__(self, host, port):
    SocketIf.__init__(self, host, port)
    
    self.rxPacketCount = 0
    self.txPacketCount = 0

    self.buffersize = Constant.DATABUFFERSIZE
    self.msgPip = []

    self.packetCount = 0

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

  @QtCore.pyqtSlot(str, name='')
  def update(self, dataList):
    self.updateStatus = True
    self.dataList = dataList

  def sendACK(self):
    cmd = "A"
    length = 0

    pac = pack('<cBI', cmd, length, self.packetCount)
    pac += 'end'
    length = len(pac)
    pac = pac[0] + pack('B', length) + pac[2:]


    if self.addr != 0:
      # print 'sending ACK' + str(self.packetCount)
      # print converInHex(pac)
      self.sock.sendto(pac, self.addr)
      # self.packetCount +=1

    outLogger.info("cmd: " + str(cmd) + " length: " + str(length) + " packetCount: " + str(self.packetCount))


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



    length = 15


    pac = pack('<cBBiiiiiI', cmd, length, di, servo0, servo1, servo2, servo3, speed, self.packetCount)
    pac += 'end'
    length = len(pac)
    pac = pac[0] + pack('B', length) + pac[2:]


    if self.addr != 0:
      print 'sending pack' + str(self.packetCount)
      # print converInHex(pac)
      self.sock.sendto(pac, self.addr)
      self.packetCount +=1

    outLogger.info(converInHex(pac))
    outLogger.info("cmd: " + str(cmd) + " length: " + str(length) + " di: " + str(di) + " servo: [" + str(servo0) + ", " + str(servo1) + ", " + str(servo2) + ", " + str(servo3) + "] s: " + str(speed) + " packetCount: " + str(self.packetCount))


  def run(self):

    print "Start wifi connection"

    # UPD_IP = ''
    # UPD_PORT = 55555
    data = ''

    t = time()
    
    count = 0
    t2 = time()

    # from time import time
    # self.t2 = time()
    # self.count = 0

    # self.count += 1
    # if time() - self.t2 > 5:
    #   print self.count / 5
    #   self.count = 0
    #   self.t2 = time()

    while 1:
      data = self.receiveMsg()
      if data != "":
        inLogger.info(data)
        if data[0] == 'H':
          print "receive: " + data

      if self.updateStatus == True:
        self.updateStatus = False
        self.sendNewUpdate()
        
        t = time()
        sleep(0.2)

        count+=1
        if time() - t2 > 5:
          print str(count / 5) + "Pack / Sec"
          count = 0
          t2 = time()
        
      else:
        if time() - t > 1:
          # send ack message to tell Arduino that we are still on line 
          self.sendACK()
          t = time()
          pass




if __name__ == '__main__':
  app = QApplication(sys.argv)

  command_if_thread = CommandIf('', 55555)
  command_if_thread.start()

  sys.exit(app.exec_())
  print "hi"
