import sys, thread, time
import numpy as np
sys.path.insert(0, "./lib/")

import Leap
from Model.Constent import *
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5 import QtCore

class leapListener(Leap.Listener):
	right_hand_init_point = np.array(RIGHTHAND_INITPOINT)
	oldPosition = np.array(RIGHTHAND_INITPOINT)
	rightHandResetCheck = [0, 0]

	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_frame(self, controller):
		frame = controller.frame()
		msg = ''
		li = []

		for hand in frame.hands:
			if hand.is_left:

				if hand.grab_strength < LEFT_GRABLIMIT:
					handDir =  hand.direction.to_float_array()
					handDir[0] = int(handDir[0] * 100)
					handDir[1] = int(handDir[1] * 100)
					handDir[2] = int(handDir[2] * 100)
					msg += " left: (%i, %i, %i)" % (handDir[0], handDir[1], handDir[2])
					li.append(['l', handDir])
			else:
				# If grab_strength > LEFT_GRABLIMIT, you can move, but celebrate
				if hand.grab_strength > LEFT_GRABLIMIT:

					handPos = np.array(hand.palm_position.to_float_array()).astype(int)

					self.grabLocation = (handPos + RIGHTHAND_SHIFT) * RIGHTHAND_SCALE
					self.right_hand_init_point = (handPos + RIGHTHAND_SHIFT) * RIGHTHAND_SCALE - self.oldPosition

				else:

					normal = hand.palm_normal
					direction = hand.direction
					# Calculate roll degree
					row = normal.roll * Leap.RAD_TO_DEG

					if row > 40:
						self.rightHandResetCheck[1] = 1
					elif row < -30:
						self.rightHandResetCheck[0] = 1
					
					strength = int(hand.grab_strength * 10)
					handNewPos = np.array(hand.palm_position.to_float_array()).astype(int) * RIGHTHAND_SCALE

					handOldPosition = handNewPos - self.right_hand_init_point

					self.oldPosition = handOldPosition

					#  -30 to 70 degree to reset init position
					if self.rightHandResetCheck == [1, 1]:
						print "reset right hand position"
						self.rightHandResetCheck = [0, 0]
						self.right_hand_init_point = handNewPos


					msg += " right: (%i, %i, %i) grab_strength: %i" % (handOldPosition[0], handOldPosition[1], handOldPosition[2], strength)
					li.append(['r', handOldPosition, strength])



		if (frame.hands.is_empty and frame.gestures().is_empty):
			msg  = 'No hand'
			li.append(['NoHand'])

		self.activity[0] = msg
		self.activity[1] = li


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

			# time.sleep(3)
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
