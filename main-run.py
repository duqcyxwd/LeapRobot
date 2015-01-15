import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

class LeapArm(object):
	"""docstring for LeapArm"""
	def __init__(self):
		super(LeapArm, self).__init__()

		self.mw = MainWindow()
		self.mw.show()
		self.mw.setController(self)
		self.startConnection()
		self.initSockets()
		
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


	def initSockets(self):
		pass


# run
def main():
	app = QApplication(sys.argv)
	mainwindow = LeapArm()
	# mainwindow.show()
	app.exec_()


if __name__ == '__main__':
	main()	
