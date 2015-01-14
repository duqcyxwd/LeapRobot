import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

class LeapArm(object):
	"""docstring for LeapArm"""
	def __init__(self, arg):
		super(LeapArm, self).__init__()

		self.mw = MainWindow()
		seff.mw.setController(self)
		self.initConnection()
		self.initSockets()
		
	def initConnection(self):
		pass

	def initSockets(self):
		pass


# run
def main():
	app = QApplication(sys.argv)
	mainwindow = MainWindow()
	mainwindow.show()
	app.exec_()


if __name__ == '__main__':
	main()	
