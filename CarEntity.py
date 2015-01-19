from Model.Constent import *

class CarEntity(object):
	"""docstring for CarEntity"""
	def __init__(self):
		super(CarEntity, self).__init__()
		self.speed = INITSPEED
		self.direction = INITDIR
		self.servoAngle = [INISERVOANGLE1, INISERVOANGLE2, INISERVOANGLE3, INISERVOANGLE4]

	def updateData(self, data):
		#if data changed
		#emit signal
		print 'updateData called'
		print data
		self.speed = data[0]
		self.direction = data[1]
		self.servoAngle = data[2]
		self.update()

	def update(self):
		try:
			self.widget
			self.widget.updateCarInterface()
		except Exception, e:
			raise e

	def setUI(self, widget):
		self.widget = widget
		pass

	def getSpeed(self):
		return self.speed

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
		angl = self.servoAngle
		self.servoAngle[0] += 1
		self.update()

	def servo1down(self):
		angl = self.servoAngle
		self.servoAngle[0] -= 1
		self.update()

	def servo2up(self):
		angl = self.servoAngle
		self.servoAngle[1] += 1
		self.update()

	def servo2down(self):
		angl = self.servoAngle
		self.servoAngle[1] -= 1
		self.update()

	def servo3up(self):
		angl = self.servoAngle
		self.servoAngle[2] += 1
		self.update()

	def servo3down(self):
		angl = self.servoAngle
		self.servoAngle[2] -= 1
		self.update()

	def servo4up(self):
		angl = self.servoAngle
		self.servoAngle[3] += 1
		self.update()

	def servo4down(self):
		angl = self.servoAngle
		self.servoAngle[3] -= 1
		self.update()




if __name__ == '__main__':
	carEnty = CarEntity()
	print carEnty.speed
	print carEnty.direction
