import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

class DemoImpl(QMainWindow):
	def __init__(self, *args):
		super(DemoImpl, self).__init__(*args)

		loadUi('MainWindow.ui', self)
		self.actionTesting.triggered.connect(self.testing)
		self.actionAbout_us.triggered.connect(self.openAbout)


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
		print "open New tab";

		widge = QWidget()
		# if graph != "null":
		#     self._graphControlWidget.setGraph(graph)
		#     widgetName = graph.plotType
		# else:

		widgetName = "Unknown Controller"

		self.tabWidget.addTab(widge, widgetName)
		self.tabWidget.setCurrentWidget(widge)

if __name__ == '__main__':
		
	app = QApplication(sys.argv)
	widget = DemoImpl()
	widget.show()
	sys.exit(app.exec_())
