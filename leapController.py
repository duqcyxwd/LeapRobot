import sys, thread, time

sys.path.insert(0, "./lib/")

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from PyQt5 import QtCore


class leapListener(Leap.Listener):
	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_frame(self, controller):
		frame = controller.frame()

		for hand in frame.hands:
			handType = "Left hand" if hand.is_left else "Right hand"
			if hand.is_left:
				print "left"
				# self.conl.stringSignal.emit("left")
				self.conl[0] = "left"
			else:
				self.conl[0] = "right"
				print "right"

class LeapController(QtCore.QThread):
	"""docstring for LeapController"""
 	stringSignal = QtCore.pyqtSignal(['QString'])

 	message = ["msg"]
 	oldmessage = 'msg'

	def __init__(self):
		super(LeapController, self).__init__()
		self._listener = leapListener()
		self._controller = Leap.Controller()
		self._isRunning = False

	def run(self):

		self._listener.conl = self.message
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
				self.stringSignal.emit(self.message[0])
				pass

	def stopListen(self):
		self._controller.remove_listener(self._listener)

	# #  TODO: validate this function??
	# @QtCore.pyqtSlot()
	# def stopSignal(self):
	# 	print "stop signal received"
	# 	# self.stopListen()
	# 	# self.terminate()
	# 	pass

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

		sys.exit(app.exec_())


	main()
