import sys, thread, time

sys.path.insert(0, "./lib/")

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QMessageBox
from PyQt5 import QtCore

class leapListener(Leap.Listener):
	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_frame(self, controller):
		frame = controller.frame()
		msg = ''

		for hand in frame.hands:
			if hand.is_left:
				handDir =  hand.direction.to_float_array()
				msg += ",left,%i, %i, %i" % (int(handDir[0] * 100), int(handDir[1] * 100), int(handDir[2] * 100))
			else:
				strength = hand.grab_strength
				handPos = hand.palm_position.to_float_array()
				msg += ",right,%i, %i, %i, %i" % (int(handPos[0] / 10), int(handPos[1] / 10), int(handPos[2] / 10), strength*10)
			self.activity[0] = msg
			self.activity[1] = []

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
				print "new incoming message"
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
