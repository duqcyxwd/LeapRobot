import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType

from View.robotHand import RobotHandWidget
from Model import *


form_class, base_class = loadUiType('View/setUpPage.ui')
class SetUpPage(base_class, form_class):
	def __init__(self, *args):
		super(SetUpPage, self).__init__(*args)
		self.setupUi(self)

	# connect carEntity and setup all connection between entity and action
	def setCarEntity(self, carEntity):
		self.carEntity = carEntity;
		self.carEntity.updateSignal.connect(self.updateCarInterface)

		self.inc.pressed.connect(self.carEntity.increaseSpeed)
		self.dec.pressed.connect(self.carEntity.decreaseSpeed)
		self.goleft.pressed.connect(self.carEntity.goLeft)
		self.goright.pressed.connect(self.carEntity.goRight)
		self.stop.pressed.connect(self.carEntity.stop)

		self.up1.pressed.connect(self.carEntity.servo1up)
		self.down1.pressed.connect(self.carEntity.servo1down)
		self.up2.pressed.connect(self.carEntity.servo2up)
		self.down2.pressed.connect(self.carEntity.servo2down)
		self.up3.pressed.connect(self.carEntity.servo3up)
		self.down3.pressed.connect(self.carEntity.servo3down)
		self.up4.pressed.connect(self.carEntity.servo4up)
		self.down4.pressed.connect(self.carEntity.servo4down)

		self.updateCarInterface()

	@pyqtSlot()
	def updateCarInterface(self, dataList = []):

		self.speed.setText(str(self.carEntity.getSpeed()))

		dirc = self.carEntity.getDirection()
		if dirc == 0:
			dirstr = 'left'
		elif dirc == 1:
			dirstr = 'stright'
		elif dirc == 2:
			dirstr = 'right'
		self.dir.setText(dirstr)
		
		servo = self.carEntity.getServoAngle()
		self.servo0.setText(str(servo[0]))
		self.servo1.setText(str(servo[1]))
		self.servo2.setText(str(servo[2]))
		self.servo3.setText(str(servo[3]))

		self.coordinates.setText(str(self.carEntity.rightHandXYZ))
		

	@pyqtSlot()
	def on_send_pressed(self):
		print "hi"

		speed = int(self.speed.text())

		servo0 = int(float(self.servo0.text()))
		servo1 = int(float(self.servo1.text()))
		servo2 = int(float(self.servo2.text()))
		servo3 = int(float(self.servo3.text()))


		dirction = self.carEntity.getDirection()
		data = [speed, dirction, [servo0, servo1, servo2, servo3]]
		self.carEntity.updateData(data)

	@pyqtSlot()
	def testFunction(self):
		print "Test button connection"
		pass


if __name__ == '__main__':

	app = QApplication(sys.argv)

	controllPage = ControlPage()
	controllPage.show()

	from CarEntity import CarEntity
	from time import sleep

			
	sys.exit(app.exec_())
