import sys, thread, time
import numpy as np
sys.path.insert(0, "./lib/")

import Leap
from Model.Constant import *
from Model.CommonFunction import *

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5 import QtCore

class leapListener(Leap.Listener):
	right_hand_init_point = np.array(RIGHTHAND_INITPOINT)
	oldPosition = np.array(RIGHTHAND_INITPOINT)
	rightHandResetCheck = [0, 0]

	def on_connect(self, controller):
		print "Connected to Leap"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_frame(self, controller):
		frame = controller.frame()
		msg = ''
		li = []

		hasLeftHand = False

		for hand in frame.hands:
			if hand.is_left:
				hasLeftHand = True

				if hand.grab_strength < LEFT_GRABLIMIT:

					normal = hand.palm_normal
					direction = hand.direction

					pitch = setValueWithRange(direction.pitch * Leap.RAD_TO_DEG, LEFT_HAND_PITCH_RANGE)
					rollDegree = setValueWithRange(normal.roll * Leap.RAD_TO_DEG, LEFT_HAND_ROLL_RANGE)

					# handDir =  np.array(hand.direction.to_float_array()).astype(int) * 100
					msg += " left hand, pitch: %f degree, roll: %f degree" % (pitch, rollDegree)
					li.append(['l', pitch, rollDegree])

			else:
				# If grab_strength > LEFT_GRABLIMIT, you can't move robot arm, but celebrate
				if hand.grab_strength > LEFT_GRABLIMIT and GESTUREENABLE:

					handPos = np.array(hand.palm_position.to_float_array()).astype(int)

					self.grabLocation = (handPos + RIGHTHAND_SHIFT) * RIGHTHAND_SCALE
					self.right_hand_init_point = (handPos + RIGHTHAND_SHIFT) * RIGHTHAND_SCALE - self.handOldPosition

				else:
					#  Moving arm
					strength = int(hand.grab_strength * 10)
					handNewPos = np.array(hand.palm_position.to_float_array()).astype(int) * RIGHTHAND_SCALE

					self.handOldPosition = handNewPos - self.right_hand_init_point

					self.checkResetGesture(hand)

					msg += " right: (%i, %i, %i) grab_strength: %i" % (self.handOldPosition[0], self.handOldPosition[1], self.handOldPosition[2], strength)
					li.append(['r', self.handOldPosition, strength])

		if (frame.hands.is_empty and frame.gestures().is_empty):
			msg  += ' No Hand Detected '
			li.append(['nh'])
		elif not hasLeftHand:
			msg  += " Can't detect left hand "
			li.append(['nl'])

		self.activity[0] = msg
		self.activity[1] = li

	def checkResetGesture(self, hand):
		#  Check Gesture, 
		# Calculate roll degree
		if not hand.is_left and GESTUREENABLE:
			handNewPos = np.array(hand.palm_position.to_float_array()).astype(int) * RIGHTHAND_SCALE

			row = hand.palm_normal.roll * Leap.RAD_TO_DEG
			if row > 30:
				self.rightHandResetCheck[1] = 1
			elif row < -30:
				self.rightHandResetCheck[0] = 1

			if (self.rightHandResetCheck == [1, 1]):
				print "reset right hand position"
				self.rightHandResetCheck = [0, 0]
				# self.right_hand_init_point = handNewPos + RIGHTHAND_SHIFT
				self.right_hand_init_point = handNewPos


class LeapController(QtCore.QThread):
	"""docstring for LeapController"""
	leapUpdateSignal = QtCore.pyqtSignal(['QString'])
	leapUpdateSignalInlist = QtCore.pyqtSignal([list])


	message = ["msg", []]
	oldmessage = 'msg'

	def __init__(self):
		super(LeapController, self).__init__()
		self._listener = leapListener()
		self._controller = Leap.Controller()
		self._isRunning = False

	def run(self):

		self._listener.activity = self.message
		self._controller.add_listener(self._listener)

		self._isRunning = True

		while self._isRunning:
			count = 0

			time.sleep(0.1)
			# print "leapController running"
			# print "this message: " + self.message[0]

			if self.message[0] != self.oldmessage:
				self.oldmessage = self.message[0]
				self.leapUpdateSignal.emit(self.message[0])
				self.leapUpdateSignalInlist.emit(self.message[1])
				pass

	def stopListen(self):
		self._controller.remove_listener(self._listener)

if __name__ == "__main__":
	def main():
		app = QtCore.QCoreApplication([])

		controlThread = LeapController()
		controlThread.finished.connect(app.exit)
		controlThread.start()

		print "Press Enter to quit..."
		try:
			sys.stdin.readline()
		except KeyboardInterrupt:
			pass
		finally:
			controlThread.stopListen()
			controlThread.terminate()
			sys.exit()

		sys.exit(app.exec_())


	main()
