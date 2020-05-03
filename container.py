from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from webview import Webview

class Container(QWidget):

	captcha_loaded = pyqtSignal(QWidget)
	load_waiting = pyqtSignal(QWidget)
	send_token = pyqtSignal(str)
	request_abort = pyqtSignal(QWidget)

	def __init__(self):
		super().__init__()
		self.tab = Webview()
		self.tab.resize(400, 680)
		self.tab.captcha_loaded.connect(lambda: self.captcha_loaded.emit(self))
		self.tab.load_waiting.connect(lambda: self.load_waiting.emit(self))
		self.tab.send_token.connect(self.send_token.emit)
		self.tab.request_abort.connect(lambda: self.request_abort.emit(self))
		self.tab.hide()
		self.label_gif = QtWidgets.QLabel()
		self.label_text = QtWidgets.QLabel()
		gif = QtGui.QMovie('gifs/loading_2.gif')
		self.label_gif.setMovie(gif)
		self.label_gif.setObjectName('label_gif')
		gif.start()
		self.label_text.setText('Waiting for captcha')
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.tab, alignment=QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_gif, alignment=QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_text, alignment=QtCore.Qt.AlignCenter)
		layout.setContentsMargins(0, 10, 0, 0)
		self.setLayout(layout)

		self.task_id = None

	def resizeEvent(self, e):
		print(e.size())