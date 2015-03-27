from Model.Constant import *
from PyQt5 import QtCore
import numpy as np


from Model.CommonFunction import calculateFromXYZToDegree,  setValueWithinLimit, convertRatio


class CarEntity(QtCore.QObject):
	"""docstring for CarEntity"""

	updateSignal = QtCore.pyqtSignal([list])
	updateSignalForWifi = QtCore.pyqtSignal([list])

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

			elif command[0] == 'nl':
				self.setSpeed(INITSPEED)

			elif command[0] == 'nh':
				self.stop()

			elif command[0] == 'r':

				coordinator = command[1] 
				self.rightHandXYZ = coordinator

				command[2] = setValueWithinLimit(command[2], CLIPPERMIN_HAND_LIMIT, CLIPPERMAX_HAND_LIMIT)
				grabStrength = (command[2] - CLIPPERMIN_HAND_LIMIT) * (CLIPPERMAX - CLIPPERMIN) / (CLIPPERMAX_HAND_LIMIT - CLIPPERMIN_HAND_LIMIT) + CLIPPERMIN

				if self.servoAngle[3] < 5 and grabStrength > 6:
					self.servoAngle[3] = grabStrength
				else:
					angle = calculateFromXYZToDegree(coordinator[0], coordinator[1], coordinator[2], ARM_VERTICAL_L*10.0, ARM_HORIZONTAL_K*10.0, HAND_LENGTH_H*10.0)

					# If that Angle is reachable 
					if angle != False:
						angle.append(grabStrength)
						self.setAngle(angle)
					else:
						self.servoAngle[3] = grabStrength

		self.update()


	def updateData(self, data):
		#if data changed 
		#emit signal
		self.speed = data[0]
		self.direction = data[1]
		self.servoAngle = data[2]
		self.update()

	def update(self):

		if self.isReady:
			# To be verify
			updateMsg = [self.speed, self.direction] + self.servoAngle
			self.updateSignal.emit(updateMsg)

			updateMsg =  self.getArduinoNum()
			# updateMsg = [self.speed, self.direction] + self.servoAngle

			self.updateSignalForWifi.emit(updateMsg)

	def getArduinoNum(self):
		arduinoPWM = [0, 0 , 0, 0]
 		arduinoPWM[0] = int(round(self.servoAngle[0]*8.0/(-3.0)+510.0))
 		arduinoPWM[0] = setValueWithinLimit(arduinoPWM[0], LEFTSERVOMAX_PWN, LEFTSERVOMIN_PWN)
 		
 		arduinoPWM[1] = int(round(self.servoAngle[1]*20.0/(9.0)+240.0))
 		arduinoPWM[1] = setValueWithinLimit(arduinoPWM[1], RIGHTSERVOMIN_PWN, RIGHTSERVOMAX_PWN)

 		arduinoPWM[2] = int(round(self.servoAngle[2]*8.0/3.0+360.0))
 		arduinoPWM[2] = setValueWithinLimit(arduinoPWM[2], BOTSERVOMIN_PWN, BOTSERVOMAX_PWN)

 		arduinoPWM[3] = int(round(convertRatio(self.servoAngle[3], CLIPPERMIN, CLIPPERMAX, CLIPPERMIN_PWM, CLIPPERMAX_PWM)))
 		arduinoPWM[3] = setValueWithinLimit(arduinoPWM[3], CLIPPERMIN_PWM, CLIPPERMAX_PWM)

 		speed = self.speed

		if speed < MINIMOVESPEED and speed > (-1 * MINIMOVESPEED):
 			speed = 0


 		if self.direction != 1:
 			speed = int(speed * 1.2)
 	
		return [speed, self.direction] + arduinoPWM

	def getSpeed(self):
		return self.speed

	def reset(self):
		self.setSpeed(INITSPEED)
		self.setDirection(INITDIR)
		self.setAngle([INISERVOANGLE1, INISERVOANGLE2, INISERVOANGLE3, INISERVOANGLE4])

	def setSpeedByCalculate(self, angle):
		self.speed = int(angle * LEFT_HAND_SPEED_CONSTANT)

	def setSpeed(self, speed):
		self.speed = speed
		self.update()

	def increaseSpeed(self):
		self.speed += 8
		self.update()
		pass

	def decreaseSpeed(self):
		self.speed -= 8
		self.update()
		pass

	def stop(self):
		self.reset()
		self.update()

	def getDirection(self):
		return self.direction

	def setDirection(self, direction):
		self.direction = direction
		self.update()

	def setDirectionByCalculate(self, direction):
		if direction > LEFT_HAND_DIRECTION_CONSTANT:
			self.direction = 0
		elif direction < -1 * LEFT_HAND_DIRECTION_CONSTANT:
			self.direction = 2
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


	# Changing Data By Changing the XYZ
	# def servo1upByXYZ(self):
	# 	self.rightHandXYZ[0] += 1
	# 	self.updateAngleFromSavedXYZ()


	# def servo1downByXYZ(self):
	# 	self.rightHandXYZ[0] -= 1
	# 	self.updateAngleFromSavedXYZ()


	# def servo2upByXYZ(self):
	# 	self.rightHandXYZ[1] += 1
	# 	self.updateAngleFromSavedXYZ()


	# def servo2downByXYZ(self):
	# 	self.rightHandXYZ[1] -= 1
	# 	self.updateAngleFromSavedXYZ()


	# def servo3upByXYZ(self):
	# 	self.rightHandXYZ[2] += 1
	# 	self.updateAngleFromSavedXYZ()


	# def servo3downByXYZ(self):
	# 	self.rightHandXYZ[2] -= 1
	# 	self.updateAngleFromSavedXYZ()


	# def updateAngleFromSavedXYZ(self):
	# 	angle = calculateFromXYZToDegree(self.rightHandXYZ[0], self.rightHandXYZ[1], self.rightHandXYZ[2], ARM_VERTICAL_L*10.0, ARM_HORIZONTAL_K*10.0, HAND_LENGTH_H*10.0)
	# 	angle.append(self.servoAngle[3])
	# 	self.servoAngle = angle
	# 	self.update()




if __name__ == '__main__':
	carEnty = CarEntity()
	print carEnty.speed
	print carEnty.direction
