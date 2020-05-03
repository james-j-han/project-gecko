from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

import json

class Account(QWidget):

	update_cookies = pyqtSignal(str, str, int)
	delete_account = pyqtSignal(int)

	def __init__(self, account_id=None, account_name=None, account_store=None, account_cookies=None):
		super().__init__()
		self.account_id = account_id
		self.account_name = account_name
		self.account_store = account_store
		if account_cookies:
			self.account_cookies = json.loads(account_cookies)
		else:
			self.account_cookies = None

		self.w_account_id = QtWidgets.QTableWidgetItem(self.account_id)
		self.w_account_id.setData(QtCore.Qt.UserRole, self.account_id)
		self.w_account_name = QtWidgets.QTableWidgetItem(self.account_name)
		self.w_account_name.setTextAlignment(QtCore.Qt.AlignCenter)
		self.w_account_store = QtWidgets.QTableWidgetItem(self.account_store)
		self.w_account_store.setTextAlignment(QtCore.Qt.AlignCenter)

		self.pb_start = QtWidgets.QPushButton()
		self.pb_start.clicked.connect(self.login)
		self.pb_start.setFixedSize(20, 20)
		self.pb_start.setFocusPolicy(QtCore.Qt.NoFocus)
		self.pb_start.setObjectName('pb_account_play')
		self.pb_refresh = QtWidgets.QPushButton()
		# self.pb_refresh.clicked.connect(self.refresh)
		self.pb_refresh.setFixedSize(20, 20)
		self.pb_refresh.setFocusPolicy(QtCore.Qt.NoFocus)
		self.pb_refresh.setObjectName('pb_account_refresh')
		self.pb_delete = QtWidgets.QPushButton()
		self.pb_delete.clicked.connect(lambda: self.delete_account.emit(self.account_id))
		self.pb_delete.setFixedSize(20, 20)
		self.pb_delete.setFocusPolicy(QtCore.Qt.NoFocus)
		self.pb_delete.setObjectName('pb_account_delete')

		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(3, 3, 3, 3)
		layout.setAlignment(QtCore.Qt.AlignCenter)
		layout.addWidget(self.pb_start)
		layout.addWidget(self.pb_refresh)
		layout.addWidget(self.pb_delete)
		self.w_actions = QtWidgets.QWidget()
		self.w_actions.setLayout(layout)

		self.cookie_jar = QNetworkCookieJar()

	def login(self):
		self.view = QWebEngineView()
		self.cookie_store = self.view.page().profile().cookieStore()
		for cookie in self.account_cookies.values():
			c = QNetworkCookie()
			c.setDomain(cookie['domain'])
			c.setName(bytes(cookie['name'], 'utf-8'))
			c.setValue(bytes(cookie['value'], 'utf-8'))
			c.setPath(cookie['path'])
			c.setExpirationDate(QtCore.QDateTime().fromString(cookie['expire']))
			self.cookie_store.setCookie(c)
		self.view.load(QtCore.QUrl(self.account_store))
		self.view.resize(800, 600)
		self.view.show()

	# def refresh(self):
	# 	self.page = QWebEnginePage()
	# 	self.cookie_store = self.page.profile().cookieStore()
	# 	for cookie in self.account_cookies.values():
	# 		c = QNetworkCookie()
	# 		c.setDomain(cookie['domain'])
	# 		c.setName(bytes(cookie['name'], 'utf-8'))
	# 		c.setValue(bytes(cookie['value'], 'utf-8'))
	# 		c.setPath(cookie['path'])
	# 		c.setExpirationDate(QtCore.QDateTime().fromString(cookie['expire']))
	# 		self.cookie_store.setCookie(c)
	# 	self.cookie_store.cookieAdded.connect(self.on_cookie_added)
	# 	self.page.load(QtCore.QUrl(self.account_store))
	# 	self.page.loadFinished.connect(self.update)

	# def on_cookie_added(self, cookie):
	# 	self.cookie_jar.insertCookie(cookie)

	# def update(self):
	# 	cookie_dict = {}
	# 	cookie_list = self.cookie_jar.allCookies()
	# 	for cookie in cookie_list:
	# 		index = cookie_list.index(cookie)
	# 		name = cookie.name().data().decode()
	# 		value = cookie.value().data().decode()
	# 		domain = cookie.domain()
	# 		path = cookie.path()
	# 		expire = cookie.expirationDate().toString()
	# 		cookie_dict[index] = {
	# 			'name': name,
	# 			'value': value,
	# 			'domain': domain,
	# 			'path': path,
	# 			'expire': expire
	# 		}
	# 	self.update_cookies.emit('account_cookies', json.dumps(cookie_dict), self.account_id)