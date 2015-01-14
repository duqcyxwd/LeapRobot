import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from controlPage import ControlPage

class MainWindow(QMainWindow):
	def __init__(self, *args):
		super(MainWindow, self).__init__(*args)

		loadUi('MainWindow.ui', self)
		self.actionTesting.triggered.connect(self.testing)
		self.actionAbout_us.triggered.connect(self.openAbout)

		self._controlPage = "null"


	def testing(self):
		for s in "This is a demo".split(" "):
			self.logList.addItem(s)
		print "Testing";

	def openAbout(self):

		message = "This is Leap-Robotic control program."
		reply = QMessageBox.information(self,
				"QMessageBox.information()", message)

	@pyqtSlot()
	def on_newtab_clicked(self):
		print "open/focus on control page";

		if self._controlPage == "null":
			widgetName = "control"
			self._controlPage = ControlPage(self)
			self.tabWidget.addTab(self._controlPage, widgetName)

		self.tabWidget.setCurrentWidget(self._controlPage)

if __name__ == '__main__':
		
	app = QApplication(sys.argv)
	widget = MainWindow()
	widget.show()
	sys.exit(app.exec_())
