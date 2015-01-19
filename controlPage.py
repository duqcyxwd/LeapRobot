import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType

from robotHand import GLWidget


app = QApplication(sys.argv)
form_class, base_class = loadUiType('controlPage.ui')
class ControlPage(base_class, form_class):
	# updateSignal = pyqtSignal(list)

	def __init__(self, *args):
		super(ControlPage, self).__init__(*args)
		self.setupUi(self)

		handWidget = GLWidget()
		self.robothandLayout.addWidget(handWidget)

		# self.carLayout.addWidget()

	
	def setCarEntity(self, carEntity):
		self.carEntity = carEntity;
		carEntity.setUI(self)


		self.inc.pressed.connect(self.carEntity.increaseSpeed)
		self.dec.pressed.connect(self.carEntity.decreaseSpeed)
		self.goleft.pressed.connect(self.carEntity.goLeft)
		self.goright.pressed.connect(self.carEntity.goRight)

		self.up1.pressed.connect(self.carEntity.servo1up)
		self.down1.pressed.connect(self.carEntity.servo1down)
		self.up2.pressed.connect(self.carEntity.servo2up)
		self.down2.pressed.connect(self.carEntity.servo2down)
		self.up3.pressed.connect(self.carEntity.servo3up)
		self.down3.pressed.connect(self.carEntity.servo3down)
		self.up4.pressed.connect(self.carEntity.servo4up)
		self.down4.pressed.connect(self.carEntity.servo4down)


		# self.up1.pressed.connect(self.updateModel)
		# self.updateSignal.connect(self.carEntity.updateData)

		self.updateCarInterface()


	# def updateModel(self):
	# 	self.updateSignal.emit([50, 1, [2, 3, 4, 5]])

	def updateCarInterface(self):
		self.speedLabel.setText(str(self.carEntity.getSpeed()))

		dirc = self.carEntity.getDirection()
		if dirc == 0:
			dirstr = 'left'
		elif dirc == 1:
			dirstr = 'stright'
		elif dirc == 2:
			dirstr = 'right'
		self.dirLabel.setText(dirstr)
		
		servo = self.carEntity.getServoAngle()
		self.servo0.setText(str(servo[0]))
		self.servo1.setText(str(servo[1]))
		self.servo2.setText(str(servo[2]))
		self.servo3.setText(str(servo[3]))

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

	controllPage = ControlPage()
	controllPage.show()

	from CarEntity import CarEntity
	from time import sleep
	carEntity = CarEntity()
	controllPage.setCarEntity(carEntity)

	sys.exit(app.exec_())
