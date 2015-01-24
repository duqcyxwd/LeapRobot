import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from Model.leapController import LeapController
from View.mainwindow import MainWindow
from Wifi.CommandIf import CommandIf
from Model.CarEntity import CarEntity

class HMobileArm(QtCore.QObject):
	"""docstring for HMobileArm"""
	def __init__(self):
		super(HMobileArm, self).__init__()

		self.app = QApplication(sys.argv)

		#start MainWindow
		self.mw = MainWindow()
		self.mw.show()
		self.mw.setController(self)

		self.carEntity = CarEntity()
		self.mw.setCarEntity(self.carEntity)

		# Connect Signal
		self.mw.startLeapSignal.connect(self.startLeapController)
		self.mw.stopLeapSignal.connect(self.stopLeapControl)

		self.mw.startConnectionSignal.connect(self.startConnection)
		self.mw.stopConnectionSignal.connect(self.stopConnection)


	def run(self):
		self.app.exec_()
		pass


	@QtCore.pyqtSlot()
	def startConnection(self):
		# if connected, or connection down, restart connection. 
		# Todo: Add icon to display connection states. 
		self.mw.addLog("start new Connection")
  		
  		self.command_if_thread = CommandIf(LOCALHOST, SERVER_PORT)

		self.carEntity.updateSignal.connect(self.command_if_thread.update)
		
  		self.command_if_thread.start()
		pass

	def stopConnection(self):
		print "stopConnection"
		self.mw.addLog("Stop Connection")
  		self.command_if_thread.start().terminate()

		pass


	def startLeapController(self):
		self.mw.addLog("start leap controller")
		
		self.leapControlThread = LeapController()
		self.leapControlThread.leapUpdateSignalInlist.connect(self.carEntity.updateFromLeap)
		self.leapControlThread.leapUpdateSignal.connect(self.mw.updateLeapControllerLabel)

		# terminate application when leap controller killed
		# self.leapControlThread.finished.connect(self.app.exit)
		
		self.leapControlThread.start()
		
		pass

	def stopLeapControl(self):
		print "stopConnection"
		self.mw.addLog("stop Leap Control")
		self.leapControlThread.stopListen()

		# TODO: Terminate will crash program, check the reason
		# self.leapControlThread.terminate()
		pass



if __name__ == '__main__':
	def main():
		h_mobileArm = HMobileArm()
		h_mobileArm.run()

	main()	
