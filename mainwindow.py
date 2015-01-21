import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from controlPage import ControlPage

class MainWindow(QMainWindow):
	startLeapSignal = QtCore.pyqtSignal()
	stopLeapSignal = QtCore.pyqtSignal()

	startConnectionSignal = QtCore.pyqtSignal()
	stopConnectionSignal = QtCore.pyqtSignal()

	testSignal = QtCore.pyqtSignal([list])

	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi('MainWindow.ui', self)
		self.actionTesting.triggered.connect(self.testing)
		self.actionAbout_us.triggered.connect(self.openAbout)

		self._controlPage = "null"

	def setController(self, controller):
		# print "set controller"

		self._controller = controller
		
	def setCarEntity(self, carEntity):
		self.carEntity = carEntity
		
	def testing(self):
		for s in "This is a demo".split(" "):
			self.logList.addItem(s)
		print "Testing";

	def openAbout(self):

		message = "This is Leap-Robotic control program."
		reply = QMessageBox.information(self,
				"QMessageBox.information()", message)

	def addLog(self, string):
		self.logList.addItem(string)
		pass


	def on_newtab_pressed(self):
		# Start Leap
		self.startLeapSignal.emit()

		print "open/focus on control page";

		if self._controlPage == "null":
			widgetName = "control"
			self._controlPage = ControlPage(self)
			self.tabWidget.addTab(self._controlPage, widgetName)

		self.tabWidget.setCurrentWidget(self._controlPage)
		self._controlPage.setCarEntity(self.carEntity)

	def on_startLeapController_pressed(self):
		self.startLeapSignal.emit()
		pass

	def on_stopLeapController_pressed(self):
		self.stopLeapSignal.emit()
		pass

	def on_stopConnection_pressed(self):
		self._controller.stopConnection()


	def on_startConnection_pressed(self):
		self._controller.startConnection()


	def on_testConnection_pressed(self):
		print "testConnection"
		self.testSignal.connect(self.testSignalFunction)
		self.testSignal.emit(['c', 'd', 1, 2, 3, [1, 2, 3]])
		
	@QtCore.pyqtSlot(list)
	def testSignalFunction(self, list):
		print list

	@QtCore.pyqtSlot(str, name='')
	def updateLeapControllerLabel(self, str):
		# print "update string: %s" % str
		self.leapInfo.setText(str)
		pass

if __name__ == '__main__':
		
	app = QApplication(sys.argv)
	widget = MainWindow()
	widget.show()

	import time
	widget.updateLeapControllerLabel("hi")
	# time.sleep(3)
	# widget.updateLeapControllerLabel("hi2")
	i = 0

	sys.exit(app.exec_())
