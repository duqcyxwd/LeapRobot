import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType


app = QApplication(sys.argv)
form_class, base_class = loadUiType('controlPage.ui')
class ControlPage(base_class, form_class):
	def __init__(self, *args):
		super(ControlPage, self).__init__(*args)
		self.setupUi(self)
		# self.setWindowTitle('control page')
		
		self.goforward.pressed.connect(self.testFunction)
	
	@pyqtSlot()

	def testFunction(self):
		print "Test button connection"
		pass

	def on_goforward_pressed(self): 
		print "goforward"

	def on_goback_pressed(self): 
		print "goback"

	def on_goleft_pressed(self): 
		print "goleft"

	def on_goright_pressed(self): 
		print "goright"

	def on_up1_pressed(self): 
		print "up1"

	def on_down1_pressed(self): 
		print "down1"

	def on_up2_pressed(self): 
		print "up2"

	def on_down2_pressed(self): 
		print "down2"

	def on_up3_pressed(self): 
		print "up3"

	def on_down3_pressed(self): 
		print "down3"

	def on_up4_pressed(self): 
		print "up4"

	def on_down4_pressed(self): 
		print "down4"


if __name__ == '__main__':

	form = ControlPage()
	form.show()
	sys.exit(app.exec_())
