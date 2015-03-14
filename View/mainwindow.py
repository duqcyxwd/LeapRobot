import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from View.controlPage import ControlPage
from View.SetUpPage import SetUpPage

class MainWindow(QMainWindow):
	startLeapSignal = QtCore.pyqtSignal()
	stopLeapSignal = QtCore.pyqtSignal()

	startConnectionSignal = QtCore.pyqtSignal()
	stopConnectionSignal = QtCore.pyqtSignal()

	testSignal = QtCore.pyqtSignal([list])

	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi('View/MainWindow.ui', self)
		self.actionTesting.triggered.connect(self.testing)
		self.actionAbout_us.triggered.connect(self.openAbout)

		self._controlPage = "null"
		self._setUpPage = "null"

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

	@QtCore.pyqtSlot()
	# NewTab for 'Start Control' button
	def on_startController_pressed(self):
		# Start Leap
		self.startLeapSignal.emit()
		# Start Wifi Connection
		# self._controller.startConnection()
		# TODO: Add start wifi controller here.

		print "open/focus on control page";

		if self._controlPage == "null":
			widgetName = "control"
			self._controlPage = ControlPage(self)
			self.tabWidget.addTab(self._controlPage, widgetName)

		self.tabWidget.setCurrentWidget(self._controlPage)
		self._controlPage.setCarEntity(self.carEntity)

	@QtCore.pyqtSlot()
	def on_startLeapController_pressed(self):
		self.startLeapSignal.emit()
		pass

	@QtCore.pyqtSlot()
	def on_stopLeapController_pressed(self):
		self.stopLeapSignal.emit()
		pass

	@QtCore.pyqtSlot()
	def on_stopConnection_pressed(self):
		self._controller.stopConnection()

	@QtCore.pyqtSlot()
	def on_startConnection_pressed(self):
		self._controller.startConnection()

	@QtCore.pyqtSlot()
	def on_setUp_pressed(self):
		print "open/focus on setUp page";
		if self._setUpPage == "null":
			widgetName = "setUp"
			self._setUpPage = SetUpPage(self)
			self.tabWidget.addTab(self._setUpPage, widgetName)

		self.tabWidget.setCurrentWidget(self._setUpPage)
		self._setUpPage.setCarEntity(self.carEntity)



	@QtCore.pyqtSlot(str, name='')
	def updateLeapControllerLabel(self, str):
		# print "update string: %s" % str
		self.leapInfo.setText(str)
		pass

if __name__ == '__main__':
		
	parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	os.sys.path.insert(0,parentdir)

	app = QApplication(sys.argv)
	widget = MainWindow()
	widget.show()

	import time
	widget.updateLeapControllerLabel("hi")
	# time.sleep(3)
	# widget.updateLeapControllerLabel("hi2")
	# 
	sys.exit(app.exec_())
