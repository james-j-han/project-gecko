from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar

from stores.store_shopify import Shopify
from stores.store_target import Target
from stores.store_bestbuy import BestBuy
from stores.store_disney import Disney
from search import Search

import time
import random
import requests
import threading
import urllib

class Task(QThread):

	update_status = pyqtSignal(str, QtWidgets.QTableWidgetItem)
	# update_proxy = pyqtSignal(str, QtWidgets.QTableWidgetItem)
	update_proxy_label = pyqtSignal(int)
	product_updated = pyqtSignal(str, QtWidgets.QTableWidgetItem)

	update_status = pyqtSignal(str, QtWidgets.QTableWidgetItem)
	update_title = pyqtSignal(str, QtWidgets.QTableWidgetItem)

	update_log = pyqtSignal(str)
	delete = pyqtSignal(int, str)
	error_delete = pyqtSignal(str)
	send_cookies = pyqtSignal(list, str)
	send_url = pyqtSignal(int, str, list)
	request_show = pyqtSignal(int)
	load_browser = pyqtSignal(int)

	request_captcha = pyqtSignal(int)
	poll_response = pyqtSignal(int)

	poll_token = pyqtSignal(int, str)
	request_abort = pyqtSignal(int)

	lock = threading.Lock()

	def __init__(self, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, ab, ac, ad):
		QThread.__init__(self)
		self.task_id = a
		self.task_name = b
		self.task_type = c
		self.store_name = d
		self.qty = e
		self.check_box_captcha = f
		self.search_type = g
		self.search = h
		self.check_box_account = i
		self.account = j
		self.profile = k
		self.billing = l
		self.check_box_proxies = m
		self.proxy_profile = n
		self.rotation = o
		self.check_box_category = p
		self.category = q
		self.check_box_size = r
		self.size = s
		self.check_box_color = t
		self.color = u
		self.retry_delay = v
		self.check_box_retry_var = w
		self.retry_var = x
		self.check_box_checkout_delay = y
		self.checkout_delay = z
		self.check_box_checkout_var = aa
		self.checkout_var = ab
		self.base_url = ac
		self.api_key = ad

		self.status = 'Ready'
		self.check_box_mask_proxy = QtWidgets.QCheckBox()
		self.check_box_mask_proxy.setCheckState(QtCore.Qt.PartiallyChecked)
		self.check_box_mask_proxy.stateChanged.connect(self.update_proxy)
		self.delay = 0
		self.countdown = 0
		self.delaying = False
		self.loading = False
		self.product_title = None
		self.abort = False
		self.solver_id = None
		self.token = None
		self.store = None
		self.keywords = None
		self.proxy = None
		self.solver_available = False
		if not self.color:
			self.color = 'N/A'

		self.finished.connect(self.stop_task)
		self.init_store()

		# image_start = QtGui.QPixmap('icons/icon_play.png')
		image_stop = QtGui.QPixmap('src/icon_stop.png')
		image_delete = QtGui.QPixmap('src/light_icon_trash.png')
		icon_start = QtGui.QIcon(QtGui.QPixmap('src/icon_play.png'))
		icon_stop = QtGui.QIcon(image_stop)
		icon_delete = QtGui.QIcon(image_delete)
		self.button_start = QtWidgets.QPushButton()
		self.button_start.setFixedSize(30, 30)
		# self.button_start.setIcon(icon_start)
		self.button_start.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_start.setObjectName('button_play')
		self.button_stop = QtWidgets.QPushButton()
		self.button_stop.setFixedSize(30, 30)
		# self.button_stop.setIcon(icon_stop)
		self.button_stop.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_stop.setObjectName('button_stop')
		self.button_stop.setEnabled(False)
		self.button_delete = QtWidgets.QPushButton()
		self.button_delete.setFixedSize(30, 30)
		# self.button_delete.setIcon(icon_delete)
		self.button_delete.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_delete.setObjectName('button_delete')

		self.button_gif = QtWidgets.QPushButton()
		self.button_gif.setFixedSize(30, 30)
		self.button_gif.setObjectName('button_gif')
		# self.label_gif = QtWidgets.QLabel()
		# self.label_gif.setFixedSize(30, 30)
		# self.label_gif.setObjectName('label_gif')
		layout = QtWidgets.QHBoxLayout()
		self.gif = QtGui.QMovie('gifs/running_2.gif')
		# self.gif.setScaledSize(QtCore.QSize(44, 44))
		self.button_gif.setIcon(QtGui.QIcon(self.gif.currentPixmap()))
		# self.button_gif.setIconSize(QtCore.QSize(30, 30))
		self.gif.frameChanged.connect(self.update_button_icon)
		# self.label_gif.setMovie(self.gif)
		self.gif.start()
		self.gif.setPaused(True)
		# layout.setSpacing(20)
		layout.setContentsMargins(6, 0, 6, 0)
		# layout.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.button_gif)
		layout.addWidget(self.button_start)
		layout.addWidget(self.button_stop)
		layout.addWidget(self.button_delete)
		self.actions = QtWidgets.QWidget()
		# self.actions.setStyleSheet("background: transparent")
		# self.actions.setAutoFillBackground(False)
		# self.actions.setObjectName('widget_actions')
		self.actions.setLayout(layout)

		# Task Name and Task Store
		# layout = QtWidgets.QVBoxLayout()
		# layout.setContentsMargins(0, 0, 0, 0)
		# name = QtWidgets.QLabel()
		# name.setText(f'{self.task_name}\n{self.store_name}')
		# name.setAlignment(QtCore.Qt.AlignCenter)
		# layout.addWidget(name)
		# self.widget_task_name = QtWidgets.QWidget()
		# self.widget_task_name.setLayout(layout)

		# QTimer
		self.interval = 50
		self.timer = QtCore.QTimer()
		self.timer.setTimerType(QtCore.Qt.PreciseTimer)
		self.timer.timeout.connect(self.update_loop)

		self.widget_task_id = QtWidgets.QTableWidgetItem(self.task_id)
		self.widget_task_id.setData(QtCore.Qt.UserRole, self.task_id)
		self.widget_task_type = QtWidgets.QTableWidgetItem(self.task_type)
		self.widget_task_type.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_task_type.setData(QtCore.Qt.UserRole, self.task_id)
		self.widget_task_name = QtWidgets.QTableWidgetItem(f'{self.task_name}\n{self.store_name}')
		self.widget_task_name.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_profile = QtWidgets.QTableWidgetItem(self.profile.profile_name)
		self.widget_profile.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_product = QtWidgets.QTableWidgetItem(self.product_title)
		self.widget_product.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_size = QtWidgets.QTableWidgetItem()
		self.widget_size.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_status = QtWidgets.QTableWidgetItem(self.status)
		self.widget_status.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_proxy = QtWidgets.QTableWidgetItem(self.proxy_profile.proxy_name)
		self.widget_proxy.setTextAlignment(QtCore.Qt.AlignCenter)
		self.widget_delay = QtWidgets.QTableWidgetItem(f'{self.countdown} ms\n{self.delay} ms')
		self.widget_delay.setTextAlignment(QtCore.Qt.AlignCenter)

		self.widget_image = QtWidgets.QWidget()
		self.label_image = QtWidgets.QLabel()
		self.label_image.setFixedSize(46, 46)
		self.label_image.setObjectName('label_image')
		# self.label_image.setScaledContents(True)
		self.image_original = QtGui.QPixmap()
		self.image_small = None
		self.image_large = None
		self.label_image.setScaledContents(False)
		self.label_image.setPixmap(QtGui.QPixmap(self.image_original))
		layout_image = QtWidgets.QVBoxLayout()
		layout_image.setContentsMargins(0, 0, 0, 0)
		layout_image.setAlignment(QtCore.Qt.AlignCenter)
		layout_image.addWidget(self.label_image)
		self.widget_image.setLayout(layout_image)

		self.title_set = False
		self.src_set = False
		self.size_set = False
		self.proxy_set = False

		self.cookie_jar = QNetworkCookieJar()

		# url_data = urllib.request.urlopen(url).read()
		# image = QtGui.QImage()
		# image.loadFromData(url_data)
		# self.ui.label_picture.setPixmap(QtGui.QPixmap(image))

	def update_button_icon(self):
		self.button_gif.setIcon(QtGui.QIcon(self.gif.currentPixmap()))

	def set_font_bold(self, bold):
		font = QtGui.QFont()
		if bold:
			font.setBold(True)
		else:
			font.setBold(False)

		self.widget_task_type.setFont(font)
		self.widget_task_name.setFont(font)
		self.widget_profile.setFont(font)
		self.widget_product.setFont(font)
		self.widget_size.setFont(font)
		self.widget_status.setFont(font)
		self.widget_delay.setFont(font)
		self.widget_proxy.setFont(font)

	def get_retry_delay(self):
		delay_var = 0
		delay = int(self.retry_delay)
		if self.check_box_retry_var == QtCore.Qt.Checked:
			delay_var = int(self.retry_var)
		lower_limit = delay - delay_var
		if lower_limit < 0:
			lower_limit = 0
		upper_limit = delay + delay_var
		random_delay = random.randint(lower_limit, upper_limit + 1)
		# print('Delay range: {} - {} [{}]'.format(lower_limit, upper_limit, random_delay))
		return random_delay

	#--------------------Init Functions--------------------

	def init_store(self):
		self.keywords = Search(self.search_type, self.search).keywords

		if self.store_name == 'Custom Shopify':
			self.store = Shopify(self.base_url, self.api_key, self.keywords, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.target.com/':
			self.store = Target(self.search, self.qty, self.size, self.color, self.account, self.profile, self.billing)
		elif self.store_name == 'https://www.bestbuy.com/':
			self.store = BestBuy(self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.shopdisney.com/':
			self.store = Disney(self.search, self.qty, self.size, self.color, self.profile, self.billing)
		else:
			print('No matching store')

		self.connect_signals()

	def connect_signals(self):
		self.store.update_status.connect(lambda message: self.update_status.emit(message, self.widget_task_id))
		self.store.update_title.connect(lambda title: self.update_title.emit(title, self.widget_task_id))
		self.store.update_image.connect(self.update_image)
		self.store.request_captcha.connect(lambda: self.request_captcha.emit(self.task_id))
		self.store.poll_response.connect(lambda: self.poll_response.emit(self.task_id))

	def load_captcha(self):
		self.private_profile = QWebEngineProfile()
		print(self.private_profile.isOffTheRecord())
		self.private_page = QWebEnginePage(self.private_profile, self)
		self.captcha_window = QWebEngineView()
		self.captcha_window.setPage(self.private_page)
		self.captcha_window.loadFinished.connect(self.render_captcha)
		for cookie in self.store.cookies:
			self.captcha_window.page().profile().cookieStore().setCookie(cookie)

		self.captcha_window.load(QtCore.QUrl(self.store.captcha_url))
		self.captcha_window.show()

	def render_captcha(self):
		script = '''
		var loop = setInterval(function() {{
			if (document.getElementById('g-recaptch') === null) {{
				
			}} else {{
				var d = document.getElementById('g-recaptch');
				document.body.innerHTML = '';
				document.body.appendChild(d);
				clearInterval(loop);
			}}
		}}, 100);
		'''
		self.captcha_window.page().runJavaScript(script, self.div_call)

	def div_call(self, data):
		script = "document.getElementById('g-recaptch');"
		# script = 'd.reset();'
		self.captcha_window.page().runJavaScript(script)

	def check_response(self):
		script = '''
		grecaptcha.getResponse();
		'''
		self.captcha_window.page().runJavaScript(script, self.token_call)

	def token_call(self, data):
		print(f'DATA: {data}')
		if data:
			self.store.g_recaptcha_response = data

	# Issue with multiple streams. Multiple tasks will crash with this function.
	def update_image(self):
		url_data = urllib.request.urlopen(self.store.src).read()
		self.image_original.loadFromData(url_data)
		width = self.image_original.width()
		height = self.image_original.height()
		if width > height:
			self.image_small = self.image_original.scaledToWidth(46, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaledToWidth(232, QtCore.Qt.SmoothTransformation)
		elif height > width:
			self.image_small = self.image_original.scaledToHeight(46, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaledToHeight(232, QtCore.Qt.SmoothTransformation)
		else:
			self.image_small = self.image_original.scaled(46, 46, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaled(232, 232, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

		self.label_image.setPixmap(self.image_small)

	def update_size(self):
		self.size_set = False
		if self.store.size and not self.size_set:
			self.widget_size.setText(f'{self.store.size}')
			self.size_set = True

	def update_proxy(self):
		self.proxy_set = False
		if self.store.proxy and not self.proxy_set:
			self.widget_proxy.setText(f'{self.proxy["https"]}')
			self.proxy_set = True

	def update_product_title(self, title):
		self.product_title = title
		self.widget_product.setText(f'{title}')

	def update_product_image(self, url):
		url_data = urllib.request.urlopen(url).read()
		# image = QtGui.QImage()
		self.image_original.loadFromData(url_data)
		width = self.image_original.width()
		height = self.image_original.height()
		if width > height:
			self.image_small = self.image_original.scaledToWidth(46, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaledToWidth(232, QtCore.Qt.SmoothTransformation)
		elif height > width:
			self.image_small = self.image_original.scaledToHeight(46, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaledToHeight(232, QtCore.Qt.SmoothTransformation)
		else:
			self.image_small = self.image_original.scaled(46, 46, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
			self.image_large = self.image_original.scaled(232, 232, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

		self.label_image.setPixmap(self.image_small)
		# self.label_image.setPixmap(QtGui.QPixmap(self.image_original.scaled(46, 46, QtCore.Qt.KeepAspectRatio)))
		# self.update_image.emit(image, self.widget_task_id)

	def update_product_size(self, size):
		self.widget_size.setText(f'{size}')
		# self.update_size.emit(size, self.widget_task_id)

	def update_task_status(self, status):
		self.widget_status.setText(f'{status}')
		# self.update_status.emit(status, self.widget_task_id)

	# def update_proxy(self):
	# 	if self.check_box_mask_proxy.checkState() == QtCore.Qt.Checked:
	# 		self.widget_proxy.setText('********************')
	# 	elif self.check_box_mask_proxy.checkState() == QtCore.Qt.PartiallyChecked:
	# 		self.widget_proxy.setText(f'{self.proxy_profile.proxy_name}')
	# 	elif self.check_box_mask_proxy.checkState() == QtCore.Qt.Unchecked:
	# 		if self.proxy:
	# 			proxy = self.proxy['https']
	# 			self.widget_proxy.setText(f'{proxy}')
	# 		else:
	# 			self.widget_proxy.setText('')
	# 	else:
	# 		print('No matching state')

	def set_cookies(self, cookies, url):
		self.send_cookies.emit(cookies, url)

	def render_page(self, url, cookies):
		self.render_view = QtWebEngineWidgets.QWebEnginePage()
		for cookie in cookies:
			self.render_view.profile().cookieStore().setCookie(cookie)
		self.render_view.load(QtCore.QUrl(url))
		self.render_view.loadFinished.connect(self.get_html)

	def get_html(self):
		self.render_view.toHtml(self.callable)

	def callable(self, data):
		self.store.rendered_html = data
		self.store.rendering = False

	#--------------------Proxy Functions--------------------

	# def get_next_proxy(self):
	# 	if self.rotation == 'Sequential':
	# 		return self.proxy_profile.get_proxy()
	# 	elif self.rotation == 'Random':
	# 		pass

	#--------------------Mask Proxy Functions--------------------

	# def mask_proxies(self, state):
	# 	if state == QtCore.Qt.Checked:
	# 		self.widget_proxy.setText('********************')
	# 	elif state == QtCore.Qt.PartiallyChecked:
	# 		self.widget_proxy.setText(self.proxy_profile.proxy_name)
	# 	elif state == QtCore.Qt.Unchecked:
	# 		if self.proxy is None:
	# 			self.widget_proxy.setText(self.proxy_profile.proxy_name)
	# 		else:
	# 			self.widget_proxy.setText('{}'.format(self.proxy['https']))
	# 	else:
	# 		print('No matching check state')

	# def unmask_proxy(self):
	# 	self.line_edit_proxy.setEchoMode(QtWidgets.QLineEdit.Normal)
	# 	# Display current proxy
	# 	self.line_edit_proxy.setText('https://user:pass@127.0.0.1:3000')

	# def mask_proxy(self):
	# 	self.line_edit_proxy.setEchoMode(QtWidgets.QLineEdit.Normal)
	# 	self.line_edit_proxy.setText(self.proxy_profile.proxy_name)

	# def mask_full_proxy(self):
	# 	self.line_edit_proxy.setEchoMode(QtWidgets.QLineEdit.Password)

	#--------------------Start/Stop Functions--------------------

	def render_browser(self):
		if self.store.abck is None:
			self.cookie_jar = QNetworkCookieJar()
			self.browser = QtWebEngineWidgets.QWebEngineView()
			# url = 'https://www.bestbuy.com/'
			self.browser.load(QtCore.QUrl(self.store_name))
			self.browser.page().profile().cookieStore().deleteAllCookies()
			self.cookie_store = self.browser.page().profile().cookieStore()
			self.cookie_store.cookieAdded.connect(self.on_cookie_added)
			self.browser.loadFinished.connect(self.start_task_2)
			# self.browser.show()
		else:
			self.loading = False

	def on_cookie_added(self, cookie):
		self.cookie_jar.insertCookie(cookie)

	def start_task(self):
		# Initialize appropriate store
		self.init_store()
		self.abort = False
		# Start task
		with self.lock:
			print('Starting task [{}][{}]'.format(self.task_id, self.task_name))
		self.gif.setFileName('gifs/running_4.gif')
		self.gif.start()
		self.countdown = 0
		# self.timer.start(self.interval)
		# self.render_browser()
		self.start()

	def start_task_2(self):
		self.store.set_cookies(self.cookie_jar)
		self.loading = False

	def stop_task(self):
		print(f'Stopping task')
		# self.update_status.emit('Aborted', self.widget_task_id)
		self.abort = True
		self.solver_available = False
		self.token = None
		if self.store:
			self.store.abort = True
		self.request_abort.emit(self.task_id)
		# Stop task
		self.gif.stop()
		self.gif.setFileName('gifs/running_2.gif')
		self.gif.start()
		self.gif.setPaused(True)
		self.delaying = False
		# self.timer.stop()
		# self.terminate()
		self.quit()
		self.wait()

	def delete_task(self):
		if self.isRunning():
			self.error_delete.emit(self.task_name)
		else:
			self.delete.emit(self.task_id, self.task_name)

	def enable_start(self):
		self.button_start.setEnabled(True)
		self.button_stop.setEnabled(False)
		self.button_delete.setEnabled(True)

	def enable_stop(self):
		self.button_stop.setEnabled(True)
		self.button_start.setEnabled(False)
		self.button_delete.setEnabled(False)

	#--------------------Captcha--------------------

	#--------------------Main Loop--------------------

	def custom_delay(self, sleep, p=True):
		self.countdown = sleep
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

	def get_proxy(self):
		if self.proxy:
			if self.rotation == 'Sequential':
				self.proxy_profile.put_seq_proxy(self.proxy)
				self.proxy = self.proxy_profile.get_seq_proxy()
			elif self.rotation == 'Random':
				self.proxy_profile.put_ran_proxy(self.proxy)
				self.proxy = self.proxy_profile.get_ran_proxy()
			else:
				with self.lock:
					print('No matching rotation')
		else:
			if self.rotation == 'Sequential':
				self.proxy = self.proxy_profile.get_seq_proxy()
			elif self.rotation == 'Random':
				self.proxy = self.proxy_profile.get_ran_proxy()
			else:
				with self.lock:
					print('No matching rotation')

	def update_loop(self):
		# if not self.abort:
		if self.delaying:
			# Update task labels/status
			# self.update_title()
			# self.update_src()
			# self.update_size()
			# self.update_proxy()
			self.widget_status.setText(f'{self.store.status}')
			# Decrement counter for delay status and update
			self.countdown -= self.interval
			if self.countdown <= 0:
				self.widget_delay.setText(f'0 ms\n{self.delay} ms')
				self.delaying = False
			else:
				self.widget_delay.setText(f'{self.countdown} ms\n{self.delay} ms')

	def run(self):
		while True:
			if self.abort:
				break
			else:
				if self.countdown > 0:
					self.msleep(self.interval)
					self.countdown -= self.interval
				else:
					self.get_proxy()
					self.store.proxy = self.proxy
					self.delay = self.get_retry_delay()
					for step in self.store.steps[self.store.current_step:]:
						if self.abort:
							break
						else:
							if step():
								continue
							else:
								self.countdown = self.delay
								break
						break

		# while not self.abort:
		# 	if self.delaying:
		# 		self.msleep(self.interval)
		# 	else:
		# 		self.get_proxy()
		# 		self.store.proxy = self.proxy
		# 		self.delay = self.get_retry_delay()
		# 		for step in self.store.steps:
		# 			if self.abort:
		# 				break
		# 			else:
		# 				# self.load_browser.emit(self.task_id)
		# 				# self.render_browser()
		# 				# self.loading = True
		# 				# while self.loading:
		# 				# 	self.msleep(self.interval)
		# 				if step():
		# 					continue
		# 				else:
		# 					self.countdown = self.delay
		# 					self.delaying = True
		# 					break

		# while not self.store.status['checkout_successful']:
		# 	# self.label_image.clear()
		# 	# self.widget_product.setText('')
		# 	# self.widget_size.setText('')
		# 	while self.delaying:
		# 		self.msleep(self.interval)

		# 	if self.abort:
		# 		break

		# 	self.get_proxy()
		# 	self.store.proxy = self.proxy
			
		# 	with self.lock:
		# 		print('Task [{}][{}] proxy: {}'.format(self.task_id, self.task_name, self.proxy['https']))
		# 	self.update_proxy()
		# 	self.update_proxy_label.emit(self.task_id)
		# 	self.delay = self.get_retry_delay()
		# 	with self.lock:
		# 		print('Task [{}][{}] delay: {}'.format(self.task_id, self.task_name, self.delay))
		# 	start = time.time()
		# 	while not self.store.status['checkout_successful']:
		# 		if self.abort:
		# 			break
		# 		else:
		# 		# try:
		# 			# Captcha
		# 			if self.store.status['captcha_detected']:
		# 				self.update_status.emit('Waiting for captcha', self.widget_task_id)
		# 				while self.token is None:
		# 					if self.abort:
		# 						break
		# 					else:
		# 						if not self.solver_available:
		# 							self.solver_available = True
		# 							print('Emitting request for captcha')
		# 							self.request_captcha.emit(self.task_id, self.store.checkout_url)
		# 					self.custom_delay(500, p=False)

		# 				if self.abort:
		# 					break
		# 				else:
		# 					self.store.token = self.token
		# 					self.token = None
		# 					self.store.status['captcha_detected'] = False
		# 			# Render javascript
		# 			# if self.store.status['render_html']:
		# 			# 	pass
		# 			# Main task loop
		# 			if self.store.status['search_all_products']:
		# 				if self.store.status['add_to_cart']:
		# 					if self.store.status['start_checkout']:
		# 						if self.store.status['submit_info']:
		# 							if self.store.status['submit_shipping']:
		# 								if self.store.status['submit_payment']:
		# 									if self.store.verify_checkout():
		# 										end = time.time()
		# 										duration = round(end - start, 3)
		# 										self.update_status.emit('Checkout success [{} seconds]'.format(duration), self.widget_task_id)
		# 										# self.update_log.emit('Task [{}] checkout success'.format(self.task_name))
		# 										self.store.status['checkout_successful'] = True
		# 										self.abort = True
		# 										break
		# 									else:
		# 										# self.update_status.emit('Verifying checkout', self.widget_task_id)
		# 										# self.update_log.emit('Task [{}] verifying checkout'.format(self.task_name))
		# 										self.store.status['checkout_successful'] = False
		# 										self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 										# self.msleep(delay)
		# 										# self.custom_delay(self.delay)
		# 										self.countdown = self.delay
		# 										self.delaying = True
		# 										break
		# 								else:
		# 									# self.update_status.emit('Submitting payment', self.widget_task_id)
		# 									# self.update_log.emit('Task [{}] submitting payment'.format(self.task_name))
		# 									if self.store.submit_payment():
		# 										self.store.status['submit_payment'] = True
		# 									else:
		# 										self.store.status['submit_payment'] = False
		# 										self.store.status['submit_shipping'] = False
		# 										self.store.status['submit_info'] = False
		# 										self.store.status['start_checkout'] = False
		# 										self.store.status['add_to_cart'] = False
		# 										self.store.status['search_all_products'] = False
		# 										# self.update_status.emit('Payment error', self.widget_task_id)
		# 										self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 										# self.msleep(delay)
		# 										# self.custom_delay(self.delay)
		# 										self.countdown = self.delay
		# 										self.delaying = True
		# 										break
		# 							else:
		# 								# self.update_status.emit('Submitting shipping', self.widget_task_id)
		# 								# self.update_log.emit('Task [{}] submitting shipping'.format(self.task_name))
		# 								if self.store.submit_shipping():
		# 									self.store.status['submit_shipping'] = True
		# 								else:
		# 									self.store.status['submit_shipping'] = False
		# 									self.store.status['submit_info'] = False
		# 									self.store.status['start_checkout'] = False
		# 									self.store.status['add_to_cart'] = False
		# 									self.store.status['search_all_products'] = False
		# 									# self.update_status.emit('Shipping error', self.widget_task_id)
		# 									self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 									# self.msleep(delay)
		# 									# self.custom_delay(self.delay)
		# 									self.countdown = self.delay
		# 									self.delaying = True
		# 									break
		# 						else:
		# 							# self.update_status.emit('Submitting information', self.widget_task_id)
		# 							# self.update_log.emit('Task [{}] submitting information'.format(self.task_name))
		# 							if self.store.submit_info():
		# 								self.store.status['submit_info'] = True
		# 							else:
		# 								self.store.status['submit_info'] = False
		# 								self.store.status['start_checkout'] = False
		# 								self.store.status['add_to_cart'] = False
		# 								self.store.status['search_all_products'] = False
		# 								# self.update_status.emit('Information error', self.widget_task_id)
		# 								self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 								# self.msleep(delay)
		# 								# self.custom_delay(self.delay)
		# 								self.countdown = self.delay
		# 								self.delaying = True
		# 								break
		# 					else:
		# 						# self.update_status.emit('Starting checkout', self.widget_task_id)
		# 						# self.update_log.emit('Task [{}] starting checkout'.format(self.task_name))
		# 						if self.store.start_checkout():
		# 							self.store.status['start_checkout'] = True
		# 						else:
		# 							self.store.status['start_checkout'] = False
		# 							self.store.status['add_to_cart'] = False
		# 							self.store.status['search_all_products'] = False
		# 							self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 							# self.msleep(delay)
		# 							# self.custom_delay(self.delay)
		# 							self.countdown = self.delay
		# 							self.delaying = True
		# 							break
		# 				else:
		# 					# self.update_status.emit('Adding to cart', self.widget_task_id)
		# 					# self.update_log.emit('Task [{}] adding to cart'.format(self.task_name))
		# 					if self.store.add_to_cart():
		# 						# self.update_status.emit('Carted', self.widget_task_id)
		# 						# self.update_log.emit('Task [{}] carted'.format(self.task_name))
		# 						self.store.status['add_to_cart'] = True
		# 					else:
		# 						# self.update_status.emit('Could not cart', self.widget_task_id)
		# 						# self.update_log.emit('Task [{}] could not cart'.format(self.task_name))
		# 						self.store.status['add_to_cart'] = False
		# 						self.store.status['search_all_products'] = False
		# 						self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 						# self.msleep(delay)
		# 						# self.custom_delay(self.delay)
		# 						self.countdown = self.delay
		# 						self.delaying = True
		# 						break
		# 			else:
		# 				# self.update_status.emit('Searching for product', self.widget_task_id)
		# 				# self.update_log.emit('Task [{}] searching for product'.format(self.task_name))
		# 				if self.store.search_all_products():
		# 					self.store.status['search_all_products'] = True
		# 				else:
		# 					self.store.status['search_all_products'] = False
		# 					self.update_log.emit('Task [{}] retrying in [{}] milliseconds'.format(self.task_name, self.delay))
		# 					with self.lock:
		# 						print('Task [{}][{}] retrying in [{}] milliseconds'.format(self.task_id, self.task_name, self.delay))
		# 					# self.msleep(delay)
		# 					# self.custom_delay(self.delay)
		# 					self.countdown = self.delay
		# 					self.delaying = True
		# 					break
		# 		# except Exception as e:
		# 		# 	with self.lock:
		# 		# 		print('[ERROR]: {}'.format(e))
		# 		# 		# with open('main.txt', mode='a') as f:
		# 		# 		# 	f.write('{}\n'.format(e))
		# 		# 	self.abort = True
		# 		# 	self.update_status.emit('Aborted: Fatal error', self.widget_task_id)
		# 		# 	self.update_log.emit('Task [{}] [ERROR]: {}'.format(self.task_name, e))
		# 		# 	break
		# 		# finally:
		# 		# 	with self.lock:
		# 		# 		print('Task [{}][{}] looping'.format(self.task_id, self.task_name))