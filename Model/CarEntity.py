from Model.Constant import *
from PyQt5 import QtCore
import numpy as np

from Model.CommonFunction import calculateFromXYZToDegree


class CarEntity(QtCore.QObject):
	"""docstring for CarEntity"""

	updateSignal = QtCore.pyqtSignal([list])

	def __init__(self):
		super(CarEntity, self).__init__()

		self.isReady = False

		self.setSpeed(INITSPEED)
		self.setDirection(INITDIR)
		self.setAngle([INISERVOANGLE1, INISERVOANGLE2, INISERVOANGLE3, INISERVOANGLE4])
		self.rightHandXYZ = [1, 1, 1]

		self.dataChangeRateByButton = GRAPH_BUTTON_CHANGE_RATE
		self.isReady = True

	def updateFromLeap(self, commandList):
		for command in commandList:
			if command[0] == 'l':
				self.setSpeedByCalculate(command[1])
				self.setDirectionByCalculate(command[2])

			elif command[0] == 'nl' or command[0] == 'nh':
				self.setSpeed(0)
				self.direction = 1

			elif command[0] == 'r':

				coordinator = command[1] 
				self.rightHandXYZ = coordinator
				grabStrength = command[2]

				angle = calculateFromXYZToDegree(coordinator[0], coordinator[1], coordinator[2], 70, 60, 20)
				
				# If that Angle is reachable 
				if angle != False:
					angle.append(grabStrength)
					self.setAngle(angle)

		self.update()


	def updateData(self, data):
		#if data changed
		#emit signal
		# print 'updateData called'
		# print data
		self.speed = data[0]
		self.direction = data[1]
		self.servoAngle = data[2]
		self.update()

	def update(self):
		if self.isReady:
			updateMsg = [self.speed, self.direction, self.servoAngle[0], self.servoAngle[1], self.servoAngle[2], self.servoAngle[3]]
			self.updateSignal.emit(updateMsg)

	def getSpeed(self):
		return self.speed

	def setSpeedByCalculate(self, angle):
		self.speed = int(angle * LEFT_HAND_SPEED_CONSTANT)

	def setSpeed(self, speed):
		self.speed = speed
		self.update()

	def increaseSpeed(self):
		self.speed += 1
		self.update()
		pass

	def decreaseSpeed(self):
		self.speed -= 1
		self.update()
		pass

	def stop(self):
		self.speed = 0 
		self.update()

	def getDirection(self):
		return self.direction

	def setDirection(self, direction):
		self.direction = direction
		self.update()

	def setDirectionByCalculate(self, direction):
		if direction > LEFT_HAND_DIRECTION_CONSTANT:
			self.direction = 2
		elif direction < -1 * LEFT_HAND_DIRECTION_CONSTANT:
			self.direction = 0
		else:
			self.direction = 1

	def goLeft(self):
		if self.direction != 0:
			self.direction -= 1
		self.update()

	def goRight(self):
		if self.direction != 2:
			self.direction += 1
		self.update()


	def getServoAngle(self):
		return self.servoAngle

	def setAngle(self, servoAngle):
		self.servoAngle = servoAngle
		self.update()	

	def servo1up(self):
		self.servoAngle[0] += self.dataChangeRateByButton
		self.update()

	def servo1down(self):
		self.servoAngle[0] -= self.dataChangeRateByButton
		self.update()

	def servo2up(self):
		self.servoAngle[1] += self.dataChangeRateByButton
		self.update()

	def servo2down(self):
		self.servoAngle[1] -= self.dataChangeRateByButton
		self.update()

	def servo3up(self):
		self.servoAngle[2] += self.dataChangeRateByButton
		self.update()

	def servo3down(self):
		self.servoAngle[2] -= self.dataChangeRateByButton
		self.update()

	def servo4up(self):
		self.servoAngle[3] += self.dataChangeRateByButton
		self.update()

	def servo4down(self):
		self.servoAngle[3] -= self.dataChangeRateByButton
		self.update()



	def servo1upByXYZ(self):
		self.rightHandXYZ[0] += 1
		self.updateAngleFromSavedXYZ()


	def servo1downByXYZ(self):
		self.rightHandXYZ[0] -= 1
		self.updateAngleFromSavedXYZ()


	def servo2upByXYZ(self):
		self.rightHandXYZ[1] += 1
		self.updateAngleFromSavedXYZ()


	def servo2downByXYZ(self):
		self.rightHandXYZ[1] -= 1
		self.updateAngleFromSavedXYZ()


	def servo3upByXYZ(self):
		self.rightHandXYZ[2] += 1
		self.updateAngleFromSavedXYZ()


	def servo3downByXYZ(self):
		self.rightHandXYZ[2] -= 1
		self.updateAngleFromSavedXYZ()


	def updateAngleFromSavedXYZ(self):
		angle = calculateFromXYZToDegree(self.rightHandXYZ[0], self.rightHandXYZ[1], self.rightHandXYZ[2], 70, 60, 20)
		angle.append(self.servoAngle[3])
		self.servoAngle = angle
		self.update()




if __name__ == '__main__':
	carEnty = CarEntity()
	print carEnty.speed
	print carEnty.direction
