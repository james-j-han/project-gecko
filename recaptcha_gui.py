from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QSound
from recaptcha_ui import Ui_recaptcha_ui
from container import Container
from webview import Webview

import queue
import time

class RecaptchaGUI(QtWidgets.QWidget):

	send_token = pyqtSignal(int, str)

	def __init__(self):
		super().__init__()
		self.ui = Ui_recaptcha_ui()
		self.ui.setupUi(self)
		self.setContentsMargins(10, 10, 10, 10)
		self.ui.tab_widget.tabBar().setObjectName('tab_widget_captcha')
		# image_add_tab = QtGui.QPixmap('src/icon_light_new_tab.png')

		icon_scale = QtCore.QSize()
		icon_scale.scale(32, 32, QtCore.Qt.KeepAspectRatio)

		# icon_new_tab = QtGui.QIcon()
		# icon_new_tab.addPixmap(QtGui.QPixmap('src/icon_light_new_tab.png'), QtGui.QIcon.Normal)
		# icon_new_tab.addPixmap(QtGui.QPixmap('src/icon_new_tab.png'), QtGui.QIcon.Active)
		# icon_new_tab.addPixmap(QtGui.QPixmap('src/icon_new_tab.png'), QtGui.QIcon.Active, QtGui.QIcon.On)
		# icon_new_tab.addPixmap(QtGui.QPixmap('src/icon_light_new_tab.png'), QtGui.QIcon.Active, QtGui.QIcon.Off)

		image_add = QtGui.QPixmap('icons/icon_add_2.png')
		image_trash = QtGui.QPixmap('icons/icon_trash.png')
		image_alert = QtGui.QPixmap('src/icon_alert.png')
		# icon_add_tab = QtGui.QIcon(image_add_tab)
		icon_add = QtGui.QIcon(image_add)
		icon_trash = QtGui.QIcon(image_trash)
		icon_new_tab = QtGui.QIcon(QtGui.QPixmap('src/icon_light_new_tab.png'))
		self.icon_alert = QtGui.QIcon(image_alert)
		self.icon_empty = QtGui.QIcon()

		self.sound_alert = QSound('src/alert.wav')

		# self.push_button_new_tab = QtWidgets.QPushButton('New')
		self.push_button_new_tab = QtWidgets.QPushButton()
		self.push_button_new_tab.setObjectName('push_button_new_tab')
		# self.push_button_new_tab.setIcon(icon_new_tab)
		# self.push_button_new_tab.setIconSize(icon_scale)

		self.ui.push_button_add.setIcon(icon_add)
		self.ui.push_button_delete.setIcon(icon_trash)
		self.ui.tab_widget.setCornerWidget(self.push_button_new_tab)

		self.push_button_new_tab.clicked.connect(self.add_tab)
		self.ui.tab_widget.tabCloseRequested.connect(self.remove_tab)
		self.ui.push_button_gmail.clicked.connect(self.load_gmail)
		self.ui.tab_widget.tabBar().tabBarDoubleClicked.connect(self.rename_tab)
		self.ui.tab_widget.currentChanged.connect(self.change_tab)
		self.ui.tab_widget.currentChanged.connect(self.toggle_closable)

		self.available_containers = []
		self.unavailable_containers = []

		self.previous_index = None
		
		self.add_tab()

	# def keyPressEvent(self, event):
	# 	print(event)
	# 	if event == QtGui.QKeyEvent():

	# 	# if event.key() == QtCore.Qt.Key_Return:
	# 	# 	self.focusWidget().clearFocus()
	# 	# 	print(self.focusWidget())
	# 	# 	print('Focus cleared!')

	# def mousePressEvent(self, QMouseEvent):
	# 	print(QMouseEvent.pos())

	def eventFilter(self, obj, e):
		if e.type() == QtCore.QEvent.FocusIn:
			index = obj.parentWidget().tabAt(obj.pos())
			self.ui.tab_widget.setCurrentIndex(index)
		elif e.type() == QtCore.QEvent.MouseButtonPress:
			index = obj.parentWidget().tabAt(obj.pos())
			self.ui.tab_widget.setCurrentIndex(index)
		return QtCore.QObject.event(obj, e)

	def change_tab(self, index):
		if self.previous_index is not None:
			text = self.ui.tab_widget.tabBar().tabData(self.previous_index)
			if text:
				self.save_text(self.previous_index, text)

		self.previous_index = index

	def rename_tab(self, index):
		text = self.ui.tab_widget.tabBar().tabData(index)
		if text:
			label = QtWidgets.QLineEdit(text)
		else:
			label = QtWidgets.QLineEdit(self.ui.tab_widget.tabText(index))
		label.setFixedWidth(100)
		label.setMaxLength(20)
		label.selectAll()
		label.installEventFilter(self)
		# label.setFrame(False)
		label.textChanged.connect(lambda: self.edit_tab_data(index, label.text()))
		label.returnPressed.connect(lambda: self.save_text(index, label.text()))
		self.ui.tab_widget.tabBar().setTabButton(index, QtWidgets.QTabBar.LeftSide, label)
		self.ui.tab_widget.setTabText(index, '')
		label.setFocus()

	def edit_tab_data(self, index, text):
		self.ui.tab_widget.tabBar().setTabData(index, text)

	def save_text(self, index, text):
		self.ui.tab_widget.tabBar().setTabButton(index, QtWidgets.QTabBar.LeftSide, None)
		self.ui.tab_widget.tabBar().setTabData(index, text)
		self.ui.tab_widget.setTabText(index, text)

	def add_tab(self):
		default_tab_name = 'Tab'
		container = Container()
		container.captcha_loaded.connect(self.captcha_loaded)
		container.load_waiting.connect(self.load_waiting)
		container.send_token.connect(lambda token: self.send_token.emit(container.task_id, token))
		container.request_abort.connect(self.load_waiting)
		self.available_containers.append(container)
		index = self.ui.tab_widget.addTab(container, default_tab_name)
		self.ui.tab_widget.tabBar().setTabData(index, default_tab_name)
		self.ui.tab_widget.setCurrentIndex(index)
		self.ui.tab_widget.setContentsMargins(0, 0, 0, 0)

	def remove_tab(self, index):
		container = self.ui.tab_widget.widget(index)
		if container in self.available_containers:
			del self.available_containers[self.available_containers.index(container)]
		elif container in self.unavailable_containers:
			del self.unavailable_containers[self.unavailable_containers.index(container)]
		else:
			print('No matching containers in avail/unavail')
		self.ui.tab_widget.removeTab(index)

	def get_available_solver(self):
		try:
			container = self.available_containers.pop()
			self.unavailable_containers.append(container)
		except IndexError:
			container = None
		return container

	def load_gmail(self):
		index = self.ui.tab_widget.currentIndex()
		container = self.ui.tab_widget.widget(index)
		container.label_gif.hide()
		container.label_text.hide()
		container.tab.load_url('https://mail.google.com')
		container.tab.show()

	def load_captcha(self, task_id, url):
		container = self.get_available_solver()
		if container:
			container.task_id = task_id
			container.tab.load_url(url, captcha=True)
			return True
		else:
			return False

	def load_waiting(self, container):
		index = self.ui.tab_widget.indexOf(container)
		self.ui.tab_widget.tabBar().setTabIcon(index, self.icon_empty)
		container.task_id = None
		container.label_gif.show()
		container.label_text.show()
		container.tab.hide()
		self.available_containers.append(self.unavailable_containers.pop(self.unavailable_containers.index(container)))

	def captcha_loaded(self, container):
		self.sound_alert.play()
		index = self.ui.tab_widget.indexOf(container)
		self.ui.tab_widget.tabBar().setTabIcon(index, self.icon_alert)
		container.label_gif.hide()
		container.label_text.hide()
		container.tab.show()

	def toggle_closable(self):
		if self.ui.tab_widget.count() <= 1:
			self.ui.tab_widget.setTabsClosable(False)
		else:
			self.ui.tab_widget.setTabsClosable(True)

	def request_abort(self, task_id):
		for container in self.unavailable_containers:
			if container.task_id == task_id:
				container.tab.t.abort = True

	def avail(self):
		print(len(self.available_containers))

	def unavail(self):
		print(len(self.unavailable_containers))

	# def closeEvent(self, event):
	# 	while True:
	# 		try:
	# 			browser = self.q.get(block=False).findChild(Webview)
	# 			print('Deleting browser object {}'.format(browser))
	# 			del browser.page
	# 		except queue.Empty:
	# 			break