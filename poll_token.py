from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets, QtCore, QtGui

class PollToken(QThread):

	poll = pyqtSignal()
	request_abort = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.abort = False

	def delay(self, sleep, p=True):
		d = 0
		v = 0
		t = 0
		interval = 50
		while d <= sleep:
			if self.abort:
				break
			else:
				self.msleep(interval)
				t = d
				d += interval
				if d > sleep:
					v = interval - (d - sleep)
					self.msleep(v)
		if p:
			print('[SLEPT]: {}ms'.format(t + v))

	def run(self):
		self.abort = False
		while True:
			if self.abort:
				self.request_abort.emit()
				break
			else:
				print('[POLLING TOKEN]')
				self.poll.emit()
				self.delay(500, p=False)