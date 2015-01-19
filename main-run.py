import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from leapController import LeapController
from mainwindow import MainWindow
from CarEntity import CarEntity

class LeapArm(QtCore.QObject):
	"""docstring for LeapArm"""
	def __init__(self):
		super(LeapArm, self).__init__()

		self.app = QApplication(sys.argv)

		#start MainWindow
		self.mw = MainWindow()
		self.mw.show()
		self.mw.setController(self)

		self.carEntity = CarEntity()

		self.startConnection()
		self.initSockets()
		

		# self.connect(self.mw, QtCore.SIGNAL("startLeapSignal"), self, QtCore.SLOT("startLeapController()"))
		# self.mw.startLeapSignal.connect(self, QtCore.SLOT("startLeapController()"))
		self.mw.startLeapSignal.connect(self.startLeapController)
		self.mw.stopLeapSignal.connect(self.stopLeapControl)



		# startLeapSingnal


	def run(self):
		self.app.exec_()
		pass


	@QtCore.pyqtSlot()
	def startConnection(self):
		# start connection here
		# 
		# if connected, or connection down, restart connection. 
		# 
		# Todo: Add icon to display connection states. 
		self.mw.addLog("start new Connection")
		
		pass

	def stopConnection(self):
		print "stopConnection"
		self.mw.addLog("Stop Connection")
		pass


	def startLeapController(self):
		self.mw.addLog("start leap controller")
		
		self.leapControlThread = LeapController()
		self.leapControlThread.stringSignal.connect(self.mw.updateLeapControllerLabel)

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


	def initSockets(self):
		pass

# qtSignal ..
# startLeapSingnal
# run
def main():
	mainwindow = LeapArm()
	mainwindow.run()

if __name__ == '__main__':
	main()	
