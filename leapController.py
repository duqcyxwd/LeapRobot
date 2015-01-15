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

class LeapController(QtCore.QThread):
	"""docstring for LeapController"""
	def __init__(self):
		super(LeapController, self).__init__()
		self.listener = leapListener()
		self.controller = Leap.Controller()

	def run(self):
		self.controller.add_listener(self.listener)

		count = 0
		while count < 20:
			time.sleep(1)
			print "Increasing %d" % count
			count += 1

	def stopListen(self):
		self.controller.remove_listener(self.listener)

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
