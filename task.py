from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar

from qasync import QEventLoop

from stores.store_shopify import Shopify
from stores.store_target import Target
from stores.store_bestbuy import BestBuy
from stores.store_disney import Disney
from stores.store_hyperxgaming import HyperXGaming
from stores.store_walmart import Walmart
from stores.store_ebay import Ebay
from search import Search
from profile import Profile
from billing import Billing

import time
import random
import requests
import threading
import urllib
import asyncio

# VERSION 1.1
class Task(QThread):

	update_title = pyqtSignal(int)
	update_image = pyqtSignal(int)
	update_size = pyqtSignal(int)
	update_proxy = pyqtSignal(int)
	update_status = pyqtSignal(int)
	update_delay = pyqtSignal(int)

	update_run = pyqtSignal(int)
	update_sleep = pyqtSignal(int)

	update_proxy_label = pyqtSignal(int)
	product_updated = pyqtSignal(str, QtWidgets.QTableWidgetItem)

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

	def __init__(self, **kwargs):
		QThread.__init__(self)
		for key, value in kwargs.items():
			setattr(self, key, value)

		self.status = 'Ready'
		self.check_box_mask_proxy = QtWidgets.QCheckBox()
		self.check_box_mask_proxy.setCheckState(QtCore.Qt.PartiallyChecked)
		self.check_box_mask_proxy.stateChanged.connect(self.mask_proxy)
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
			self.color = 'N/A' # FIX THIS

		self.get_retry_delay()

		self.finished.connect(self.stop_task)
		self.init_store()

		# self.loop = asyncio.get_event_loop()
		# self.loop.run_until_complete(self.run2())
		# self.loop.create_task(self.run_2())

		# self.thread = threading.Thread(target=self.run_forever, args=(self.loop,))
		# self.thread.daemon = True

		# image_start = QtGui.QPixmap('icons/icon_play.png')
		image_stop = QtGui.QPixmap('src/icon_stop.png')
		image_delete = QtGui.QPixmap('src/light_icon_trash.png')
		icon_start = QtGui.QIcon(QtGui.QPixmap('src/icon_play.png'))
		icon_captcha = QtGui.QIcon(QtGui.QPixmap('src/captcha.png'))
		icon_stop = QtGui.QIcon(image_stop)
		icon_delete = QtGui.QIcon(image_delete)
		self.button_start = QtWidgets.QPushButton()
		self.button_start.setFixedSize(26, 26)
		# self.button_start.setIcon(icon_start)
		self.button_start.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_start.setObjectName('button_play')
		self.button_stop = QtWidgets.QPushButton()
		self.button_stop.setFixedSize(26, 26)
		# self.button_stop.setIcon(icon_stop)
		self.button_stop.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_stop.setObjectName('button_stop')
		self.button_stop.setEnabled(False)
		self.button_delete = QtWidgets.QPushButton()
		self.button_delete.setFixedSize(26, 26)
		# self.button_delete.setIcon(icon_delete)
		self.button_delete.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_delete.setObjectName('button_delete')

		self.button_captcha = QtWidgets.QPushButton()
		self.button_captcha.setFixedSize(26, 26)
		# self.button_captcha.setIcon(icon_delete)
		self.button_captcha.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_captcha.setObjectName('button_captcha')

		self.button_account = QtWidgets.QPushButton()
		self.button_account.setFixedSize(26, 26)
		self.button_account.setFocusPolicy(QtCore.Qt.NoFocus)
		self.button_account.setObjectName('button_account')

		self.button_gif = QtWidgets.QPushButton()
		self.button_gif.setFixedSize(26, 26)
		self.button_gif.setObjectName('button_gif')
		# self.label_gif = QtWidgets.QLabel()
		# self.label_gif.setFixedSize(30, 30)
		# self.label_gif.setObjectName('label_gif')
		layout = QtWidgets.QHBoxLayout()
		self.gif = QtGui.QMovie('gifs/running_2.gif')
		# self.gif.setScaledSize(QtCore.QSize(44, 44))
		self.button_gif.setIcon(QtGui.QIcon(self.gif.currentPixmap()))
		# self.button_gif.setIconSize(QtCore.QSize(30, 30))
		# self.gif.frameChanged.connect(self.update_button_icon)
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
		layout.addWidget(self.button_account)
		layout.addWidget(self.button_captcha)
		self.actions = QtWidgets.QWidget()
		# self.actions.setStyleSheet("background: transparent")
		# self.actions.setAutoFillBackground(False)
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
		self.interval = 53
		self.timer = QtCore.QTimer()
		self.timer.setTimerType(QtCore.Qt.PreciseTimer)
		self.timer.timeout.connect(self.update_loop)

		# Task ID cell
		self.widget_task_id = QtWidgets.QTableWidgetItem()
		self.widget_task_id.setData(QtCore.Qt.UserRole, self.task_id)

		# Task type cell
		self.widget_task_type = QtWidgets.QWidget()
		self.widget_task_type.setObjectName('w_task_type')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_task_type = QtWidgets.QLabel(self.task_type)
		self.label_task_type.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_task_type)
		self.widget_task_type.setLayout(layout)
		
		# Task name and store cell
		self.widget_name_store = QtWidgets.QWidget()
		self.widget_name_store.setObjectName('w_name_store')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_name_store = QtWidgets.QLabel(f'{self.task_name}\n{self.store_name}')
		self.label_name_store.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_name_store)
		self.widget_name_store.setLayout(layout)
		
		# Task profile cell
		self.widget_profile = QtWidgets.QWidget()
		self.widget_profile.setObjectName('w_profile')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_profile = QtWidgets.QLabel(f'{self.profile.profile_name}')
		self.label_profile.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_profile)
		self.widget_profile.setLayout(layout)
		
		# Task product cell
		self.widget_product = QtWidgets.QWidget()
		self.widget_product.setObjectName('w_product')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_product = QtWidgets.QLabel()
		# self.label_product.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_product)
		self.widget_product.setLayout(layout)
		
		# Task image cell
		self.widget_image = QtWidgets.QWidget()
		self.widget_image.setObjectName('w_image')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_image = QtWidgets.QLabel()
		self.label_image.setObjectName('label_image')
		self.label_image.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_image)
		self.widget_image.setLayout(layout)
		
		# Task proxy cell
		self.widget_proxy = QtWidgets.QWidget()
		self.widget_proxy.setObjectName('w_proxy')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_proxy = QtWidgets.QLabel()
		self.label_proxy.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_proxy)
		self.widget_proxy.setLayout(layout)

		# Task status cell
		self.widget_status = QtWidgets.QWidget()
		self.widget_status.setObjectName('w_status')
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		self.label_status = QtWidgets.QLabel(f'{self.store.status}')
		self.label_status.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.label_status)
		self.widget_status.setLayout(layout)
		
		# Task action cell
		self.widget_action = QtWidgets.QWidget()
		self.widget_action.setObjectName('w_action')
		self.widget_action.setContentsMargins(0, 0, 10, 0)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(4, 0, 4, 4)
		layout.addWidget(self.button_gif)
		layout.addWidget(self.button_start)
		layout.addWidget(self.button_stop)
		layout.addWidget(self.button_delete)
		layout.addWidget(self.button_account)
		layout.addWidget(self.button_captcha)
		self.widget_action.setLayout(layout)

		self.cookie_jar = QNetworkCookieJar()

	# def update_button_icon(self):
	# 	self.button_gif.setIcon(QtGui.QIcon(self.gif.currentPixmap()))

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
		delay_min = int(self.delay_min)

		delay_max = delay_min
		if self.delay_max:
			delay_max = int(self.delay_max)

		random_delay = random.randint(delay_min, delay_max)
		print(random_delay)
		return random_delay

		# delay_var = 0
		# delay = int(self.retry_delay)
		# if self.check_box_retry_var == QtCore.Qt.Checked:
		# 	delay_var = int(self.retry_var)
		# lower_limit = delay - delay_var
		# if lower_limit < 0:
		# 	lower_limit = 0
		# upper_limit = delay + delay_var
		# random_delay = random.randint(lower_limit, upper_limit + 1)
		# # print('Delay range: {} - {} [{}]'.format(lower_limit, upper_limit, random_delay))
		# return random_delay

	#--------------------Init Functions--------------------

	def init_store(self):
		self.keywords = Search(self.search_type, self.search).keywords

		if self.store_name == 'Custom Shopify':
			self.store = Shopify(self.base_url, self.api_key, self.keywords, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.target.com/':
			self.store = Target(self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.bestbuy.com/':
			self.store = BestBuy(self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.shopdisney.com/':
			self.store = Disney(self.task_type, self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.hyperxgaming.com/':
			self.store = HyperXGaming(self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.walmart.com/':
			self.store = Walmart(self.task_type, self.search, self.qty, self.size, self.color, self.profile, self.billing)
		elif self.store_name == 'https://www.ebay.com/':
			self.store = Ebay(self.task_type, self.search, self.qty, self.size, self.color, self.profile, self.billing)
		else:
			print('No matching store')

		self.connect_signals()

	def connect_signals(self):
		self.store.update_status.connect(lambda: self.update_status.emit(self.task_id))
		self.store.update_title.connect(lambda: self.update_title.emit(self.task_id))
		self.store.update_image.connect(lambda: self.update_image.emit(self.task_id))
		self.store.update_size.connect(lambda: self.update_size.emit(self.task_id))
		# self.store.update_proxy.connect(lambda: self.update_proxy.emit(self.task_id))
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

	def set_title(self):
		self.label_product.setText(f'{self.store.title}\nQty: {self.store.qty}  Size: {self.store.size}  Color: {self.store.color}')

	def set_image(self):
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
		}
		try:
			r = requests.get(self.store.src, headers=headers)
			if r.status_code == 200:
				image = QtGui.QPixmap()
				image.loadFromData(r.content)
				scaled = image.scaledToWidth(36, QtCore.Qt.SmoothTransformation)
				self.label_image.setPixmap(scaled)
		except Exception as e:
			print(f'{e}')

	def set_size(self):
		self.label_product.setText(f'{self.store.title}\nQty: {self.store.qty}  Size: {self.store.size}  Color: {self.store.color}')

	def set_status(self):
		self.label_status.setText(self.store.status)

	def set_proxy(self):
		if self.check_box_mask_proxy.checkState() == QtCore.Qt.Unchecked:
			if self.proxy:
				for value in self.proxy.values():
					self.widget_proxy.setText(value)
			else:
				self.widget_proxy.setText('localhost')

	# def set_delay(self):
	# 	self.widget_delay.setText(f'{self.delay} ms')

	def mask_proxy(self):
		if self.check_box_mask_proxy.checkState() == QtCore.Qt.Checked:
			self.widget_proxy.setText('**********')
		elif self.check_box_mask_proxy.checkState() == QtCore.Qt.PartiallyChecked:
			self.widget_proxy.setText(f'{self.proxy_profile.proxy_name}')
		elif self.check_box_mask_proxy.checkState() == QtCore.Qt.Unchecked:
			if self.proxy:
				for value in self.proxy.values():
					self.widget_proxy.setText(f'{value}')
			else:
				self.widget_proxy.setText('localhost')
		else:
			print('No matching state')

	#--------------------Start/Stop Functions--------------------

	def start_task(self):
		# if self.task_type == 'Bot':
		# 	# try:
		# 	# 	self.loop.run_until_complete(self.run_2())
		# 	# except KeyboardInterrupt:
		# 	# 	self.loop.run_until_complete(self.store.logout())
		# 	# finally:
		# 	# 	self.loop.close()
		# 	self.thread.start()
		# else:
		if not self.isRunning():
			# Initialize appropriate store
			# self.init_store()
			self.abort = False
			# Start task
			with self.lock:
				print(f'Starting task [{self.task_id}][{self.task_name}]')
			self.countdown = 0
			self.start()

	def stop_task(self):
		# if self.task_type == 'Bot':
		# 	# self.store.close()
		# 	# print(self.t.is_alive())
		# 	self.store.logout()
		# 	# raise Exception('LOL')
		# else:
		if self.isRunning():
			with self.lock:
				print(f'Stopping task [{self.task_id}][{self.task_name}]')
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
			# self.store.logout()
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

	#--------------------Status Icon--------------------

	def set_idle(self):
		pass

	def set_run(self):
		self.gif.stop()
		self.gif.setFileName('gifs/running_4.gif')
		self.gif.start()
	
	def set_sleep(self):
		self.gif.stop()
		self.gif.setFileName('gifs/running_2.gif')
		self.gif.start()

	def set_success(self):
		pass

	#--------------------Main Loop--------------------

	def update_loop(self):
		if self.countdown > 0:
			self.widget_delay.setText(f'{self.countdown} ms\n{self.delay} ms')
		else:
			self.widget_delay.setText(f'0 ms\n{self.delay} ms')

	def run(self):
		while True:
			if self.abort:
				break
			else:
				if self.countdown > 0:
					self.msleep(self.interval)
					self.countdown -= self.interval
				else:
					self.update_run.emit(self.task_id)
					self.update_delay.emit(self.task_id)
					self.proxy = self.proxies.get_proxy(self.proxy, self.rotation)
					self.update_proxy.emit(self.task_id)
					self.store.s.proxies.clear()
					self.store.s.proxies.update(self.proxy)
					self.delay = self.get_retry_delay()
					for step in self.store.steps[self.store.current_step:]:
						if self.abort:
							break
						else:
							# if step == self.store.steps[0]:
							# 	self.store.s.cookies.clear()
							
							if step():
								if step == self.store.steps[-1]:
									pass
								else:
									continue
							else:
								self.countdown = self.delay
								# self.update_sleep.emit(self.task_id)
								break

						self.abort = True
						break