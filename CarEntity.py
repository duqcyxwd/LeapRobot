from Model.Constent import *
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

		self.dataChangeRateByButton = GRAPH_BUTTON_CHANGE_RATE
		self.isReady = True

	def updateFromLeap(self, li):
		for x in li:
			if x[0] == 'l':
				self.setSpeedByCalculate(x[1][1])
				self.setdirectionByCalculate(x[1][0])
				direct = x[1][0]
				if direct > 20:
					self.direction = 2
				elif direct < -20:
					self.direction = 0
				else:
					self.direction = 1

			elif x[0] == 'NoHand':
				self.setSpeed(0)
				self.direction = 1

			elif x[0] == 'r':
				# self.servoAngle = x[1].append(x[2])
				# self.direction = self.servoAngle
				

				angle = x[1] 

				print x[1]

				angle = calculateFromXYZToDegree(angle[0], angle[1], angle[2], 80, 80, 68)
				
				angle.append(x[2])

				self.setAngle(angle)


			elif x[0] == 'RightCelebrate':

				pass



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

	def setSpeedByCalculate(self, spd):
		self.speed = spd * -1
		self.update()

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
		if direction > 2:
			self.direction = 2
		elif direction < 0:
			self.direction = 0
		else:
			self.direction = 1
		self.update()

	def setdirectionByCalculate(self, direction):
		if direction > 0:
			self.direction = 2
		else:
			self.direction = 0

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
		# hard code here

		# if servoAngle[0] > 255:
		# 	servoAngle[0] = 255
		# elif servoAngle[0] < 0:
		# 	servoAngle[0] =0

		# if servoAngle[1] > 255:
		# 	servoAngle[1] = 255
		# elif servoAngle[1] < 0:
		# 	servoAngle[1] =0

		# if servoAngle[2] > 255:
		# 	servoAngle[2] = 255
		# elif servoAngle[2] < 0:
		# 	servoAngle[2] =0

		# if servoAngle[3] > 255:
		# 	servoAngle[3] = 255
		# elif servoAngle[3] < 0:
		# 	servoAngle[3] =0

		self.servoAngle = servoAngle
		self.update()	


	def servo1up(self):
		angl = self.servoAngle
		self.servoAngle[0] += self.dataChangeRateByButton
		self.update()

	def servo1down(self):
		angl = self.servoAngle
		self.servoAngle[0] -= self.dataChangeRateByButton
		self.update()

	def servo2up(self):
		angl = self.servoAngle
		self.servoAngle[1] += self.dataChangeRateByButton
		self.update()

	def servo2down(self):
		angl = self.servoAngle
		self.servoAngle[1] -= self.dataChangeRateByButton
		self.update()

	def servo3up(self):
		angl = self.servoAngle
		self.servoAngle[2] += self.dataChangeRateByButton
		self.update()

	def servo3down(self):
		angl = self.servoAngle
		self.servoAngle[2] -= self.dataChangeRateByButton
		self.update()

	def servo4up(self):
		angl = self.servoAngle
		self.servoAngle[3] += self.dataChangeRateByButton
		self.update()

	def servo4down(self):
		angl = self.servoAngle
		self.servoAngle[3] -= self.dataChangeRateByButton
		self.update()




if __name__ == '__main__':
	carEnty = CarEntity()
	print carEnty.speed
	print carEnty.direction
