from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets, QtWebChannel, QtWebEngineCore, QtNetwork
from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar, QNetworkProxy
from PyQt5.QtWebEngineWidgets import QWebEngineView

from the_gecko_app_ui import Ui_MainWindow
# from test_window_ui import Ui_Form
# from recaptcha_ui import Ui_Form
from recaptcha_gui import RecaptchaGUI
from activation_gui import ActivationGUI
# from solver import Solver

from database import TheGeckoAppDatabase
# from local_server import LocalServer
# from captcha_token import Token
# from captcha_queue import CaptchaQueue
from task import Task
from profile import Profile
from billing import Billing
from proxy import Proxy
from account import Account
# from interceptor import Interceptor
from stylesheet import Stylesheet

import os
import sys
import datetime
import time
import requests
import urllib
import queue
import json

import gecko_utils

VERSION = 'The Gecko App v0.0.9'

class GUI(QtWidgets.QMainWindow):

	def __init__(self, db):
		super().__init__()
		# app = QtWidgets.QApplication(sys.argv)
		# MainWindow = QtWidgets.QMainWindow()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.ui.pushButton.clicked.connect(self.test)

		self.cbe_items = [
			self.ui.cbe_task_type,
			self.ui.cbe_store,
			self.ui.cbe_search_type,
			self.ui.cbe_search,
			self.ui.cbe_task_name,
			self.ui.cbe_qty,
			self.ui.cbe_account,
			self.ui.cbe_profile,
			self.ui.cbe_billing,
			self.ui.cbe_proxies,
			self.ui.cbe_rotation,
			self.ui.cbe_size,
			self.ui.cbe_color,
			self.ui.cbe_category,
			self.ui.cbe_price_range,
			self.ui.cbe_delay_range,
			self.ui.cbe_captcha
		]

		self.ui.cbe_task_type.stateChanged.connect(self.toggle_cbe_task_type)
		self.ui.cbe_store.stateChanged.connect(self.toggle_cbe_store)
		self.ui.cbe_search_type.stateChanged.connect(self.toggle_cbe_search_type)
		self.ui.cbe_search.stateChanged.connect(self.toggle_cbe_search)
		self.ui.cbe_task_name.stateChanged.connect(self.toggle_cbe_task_name)
		self.ui.cbe_qty.stateChanged.connect(self.toggle_cbe_qty)
		self.ui.cbe_account.stateChanged.connect(self.toggle_cbe_account)
		self.ui.cbe_profile.stateChanged.connect(self.toggle_cbe_profile)
		self.ui.cbe_billing.stateChanged.connect(self.toggle_cbe_billing)
		self.ui.cbe_proxies.stateChanged.connect(self.toggle_cbe_proxies)
		self.ui.cbe_rotation.stateChanged.connect(self.toggle_cbe_rotation)
		self.ui.cbe_size.stateChanged.connect(self.toggle_cbe_size)
		self.ui.cbe_color.stateChanged.connect(self.toggle_cbe_color)
		self.ui.cbe_category.stateChanged.connect(self.toggle_cbe_category)
		self.ui.cbe_price_range.stateChanged.connect(self.toggle_cbe_price_range)
		self.ui.cbe_delay_range.stateChanged.connect(self.toggle_cbe_delay_range)
		self.ui.cbe_captcha.stateChanged.connect(self.toggle_cbe_captcha)

		self.ui.check_box_account.stateChanged.connect(self.toggle_accounts)
		self.ui.check_box_proxies.stateChanged.connect(self.toggle_proxies)
		self.ui.check_box_size.stateChanged.connect(self.toggle_size)
		self.ui.check_box_color.stateChanged.connect(self.toggle_color)
		self.ui.check_box_category.stateChanged.connect(self.toggle_category)
		self.ui.check_box_price_range.stateChanged.connect(self.toggle_price_range)

		self.ui.combo_box_task_type.addItem('Normal')
		self.ui.combo_box_task_type.addItem('Monitor')
		self.ui.combo_box_task_type.addItem('Bot')

		store_disney = {
			'url': 'https://www.shopdisney.com/',
			'task_type': {
				'Normal': True,
				'Monitor': True,
				'Bot': False
			},
			'search_type': {
				'Direct Link': True,
				'Keyword': False,
				'Variant': True,
				'Webhook': False
			}
		}

		store_ebay = {
			'url': 'https://www.ebay.com/',
			'task_type': {
				'Normal': False,
				'Monitor': False,
				'Bot': True
			},
			'search_type': {
				'Direct Link': False,
				'Keyword': False,
				'Variant': False,
				'Webhook': True
			}
		}

		store_walmart = {
			'url': 'https://www.walmart.com/',
			'task_type': {
				'Normal': True,
				'Monitor': False
			},
			'search_type': {
				'Direct Link': True,
				'Keyword': False,
				'Variant': False,
				'Webhook': False
			}
		}

		store_target = {
			'url': 'https://www.target.com/',
			'task_type': {
				'Normal': True,
				'Monitor': False
			},
			'search_type': {
				'Direct Link': True,
				'Keyword': False,
				'Variant': True,
				'Webhook': False
			}
		}

		self.stores = [
			store_disney,
			store_ebay,
			store_walmart,
			store_target
		]

		self.load_stores('Normal')

		self.fallback_sitekeys = {
			'https://shop.funko.com/': '6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF',
			# 'https://shop.funko.com/': '6LcCR2cUAAAAANS1Gpq_mDIJ2pQuJphsSQaUEuc9',
			'https://www.hottopic.com/': '6LdasBsTAAAAAJ2ZY_Z60WzgpRRgZVKXnqoad77Y',
			'https://www.supremenewyork.com/': '6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz'
		}

		self.old_sizes = [200, 1000, 16]
		self.ui.frame_log.hide()
		self.ui.splitter.setSizes(self.old_sizes)

		# Initialize any necessary database tables
		# self.tgadb = TheGeckoAppDatabase('gecko.db')
		# self.tgadb.create_table_tasks()
		# self.tgadb.create_table_profiles()
		# self.tgadb.create_table_billing()
		# self.tgadb.create_table_proxies()
		# self.tgadb.create_table_solvers()
		self.tgadb = db

		# Initialize solvers
		self.captcha_window = RecaptchaGUI()
		# self.captcha_window.browser_unavailable.connect()
		self.captcha_window.send_token.connect(self.send_token)
		# self.solver_window.create_solver.connect(self.save_solver)
		# self.solver_window.start_solver.connect(self.start_solver)
		# self.solver_window.delete_solver.connect(self.delete_solver)
		# self.solver_window.stop_solvers.connect(self.stop_solvers)

		# need callback to main executable
		# self.icon_logo = QtGui.QPixmap(QtGui.QImage('src/logo_2.png').scaled(232, 232, QtCore.Qt.KeepAspectRatio))
		# self.ui.label_picture.setPixmap(self.icon_logo)
		self.proxies = {}
		self.tasks = {}
		self.task_ids = []
		self.accounts = {}
		self.profiles = {}
		self.billing = {}
		self.solvers = {}
		self.items_to_save = {}

		self.mass_edit_fields = {}
		self.shopify = {
			'base_url': None,
			'api_key': None,
			'success': None
		}
		# self.servers = {}
		# self.local_server = LocalServer()
		# self.local_server.start()
		# self.dir = QtCore.QDir()
		# self.dir.cd(self.dir.rootPath())
		# self.dir.cd('Windows')
		# self.dir.cd('System32')
		# self.dir.cd('drivers')
		# self.dir.cd('etc')
		# try:
		# 	os.chmod(self.dir.path(), 0o777)
		# 	with open('hosts.txt', 'r') as f:
		# 		hosts = f.read()
		# 	with open(os.path.join(self.dir.path(), 'hosts'), 'w') as f:
		# 		f.write(hosts)
		# except Exception as e:
		# 	self.permission_dialog('Permission Denied', '{}\n\n Please run as administrator'.format(e))

		# rx = QtCore.QRegExp('^[0-9]{1,}$')
		# rx = QtCore.QRegExp('^([1-9][0-9]*)$')
		# self.validator = QtGui.QRegExpValidator(rx, self)
		# for item in self.num_only_line_edits:
		# 	item.setValidator(self.validator)

#================================================================================
# RECAPTCHA WINDOW
#================================================================================

#================================================================================
# ICONS
#================================================================================

		# icon_start = QtGui.QIcon(QtGui.QPixmap('src/icon_play.png'))
		# icon_stop = QtGui.QIcon(QtGui.QPixmap('src/icon_stop.png'))
		# icon_delete = QtGui.QIcon(QtGui.QPixmap('src/light_icon_trash.png'))
		# icon_captcha = QtGui.QIcon(QtGui.QPixmap('src/icon_captcha.png'))
		# icon_save = QtGui.QIcon(QtGui.QPixmap('src/icon_save.png'))
		# self.ui.push_button_start_tasks.setIcon(icon_start)
		# self.ui.push_button_stop_tasks.setIcon(icon_stop)
		# self.ui.push_button_delete_all_tasks.setIcon(icon_delete)
		# self.ui.push_button_captcha.setIcon(icon_captcha)
		# self.ui.push_button_save_task.setIcon(icon_save)

		# icon_proxy = QtGui.QIcon(QtGui.QPixmap('src/icon_light_proxy.png'))
		# self.ui.check_box_mask_proxies.setIcon(icon_proxy)
		icon_scale = QtCore.QSize()
		icon_scale.scale(32, 32, QtCore.Qt.KeepAspectRatio)
		self.ui.tabWidget.setIconSize(icon_scale)

		icon_task = QtGui.QIcon()
		icon_task.addPixmap(QtGui.QPixmap('src/icon_rotate_task.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icon_task.addPixmap(QtGui.QPixmap('src/icon_rotate_light_task.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(0, icon_task)
		icon_profile = QtGui.QIcon()
		icon_profile.addPixmap(QtGui.QPixmap('src/icon_rotate_profile.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icon_profile.addPixmap(QtGui.QPixmap('src/icon_rotate_light_profile.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(1, icon_profile)
		icon_billing = QtGui.QIcon()
		icon_billing.addPixmap(QtGui.QPixmap('src/icon_rotate_card.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icon_billing.addPixmap(QtGui.QPixmap('src/icon_rotate_light_card.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(2, icon_billing)
		icon_proxy = QtGui.QIcon()
		icon_proxy.addPixmap(QtGui.QPixmap('src/icon_rotate_proxy.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icon_proxy.addPixmap(QtGui.QPixmap('src/icon_rotate_light_proxy.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(3, icon_proxy)
		icont_account = QtGui.QIcon()
		icont_account.addPixmap(QtGui.QPixmap('src/icon_rotate_account.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icont_account.addPixmap(QtGui.QPixmap('src/icon_rotate_light_account.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(4, icont_account)
		icon_settings = QtGui.QIcon()
		icon_settings.addPixmap(QtGui.QPixmap('src/icon_gear.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
		icon_settings.addPixmap(QtGui.QPixmap('src/icon_light_gear.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ui.tabWidget.setTabIcon(5, icon_settings)

#================================================================================
# TASK BUTTONS
#================================================================================

		self.ui.push_button_new_task.clicked.connect(self.new_task)
		self.ui.push_button_save_task.clicked.connect(self.save_task)

		# self.ui.label_picture.setScaledContents(False)
		# self.ui.combo_box_store.currentIndexChanged.connect(self.load_types)
		self.ui.combo_box_task_type.currentTextChanged.connect(self.load_stores)
		self.ui.combo_box_store.currentTextChanged.connect(self.load_search_options)
		self.ui.combo_box_search_type.currentTextChanged.connect(self.load_task_options)
		self.ui.push_button_start_tasks.setText('Start All')
		self.ui.push_button_start_tasks.clicked.connect(self.start_tasks)
		self.ui.push_button_stop_tasks.setText('Stop All')
		self.ui.push_button_stop_tasks.clicked.connect(self.stop_tasks)
		self.ui.push_button_delete_tasks.setText('Delete All')
		self.ui.push_button_delete_tasks.clicked.connect(self.delete_all_tasks)
		# self.ui.line_edit_retry_delay.textChanged.connect(lambda: self.update_delay_label(self.ui.label_retry, self.ui.line_edit_retry_delay, self.ui.line_edit_retry_variance))
		# self.ui.line_edit_retry_variance.textChanged.connect(lambda: self.update_delay_label(self.ui.label_retry, self.ui.line_edit_retry_delay, self.ui.line_edit_retry_variance))
		# self.ui.line_edit_checkout_delay.textChanged.connect(lambda: self.update_delay_label(self.ui.label_checkout, self.ui.line_edit_checkout_delay, self.ui.line_edit_checkout_variance))
		# self.ui.line_edit_checkout_variance.textChanged.connect(lambda: self.update_delay_label(self.ui.label_checkout, self.ui.line_edit_checkout_delay, self.ui.line_edit_checkout_variance))
		self.ui.push_button_test_custom_shopify.clicked.connect(self.test_shopify)

#================================================================================
# PROFILE BUTTONS
#================================================================================

		self.ui.push_button_new_profile.clicked.connect(self.new_profile)
		self.ui.push_button_save_profile.clicked.connect(self.save_profile)
		self.ui.push_button_delete_all_profiles.clicked.connect(self.delete_all_profiles)
		self.ui.push_button_delete_profile.clicked.connect(lambda: self.delete_profile(self.ui.list_widget_profiles.currentItem()))
		self.ui.list_widget_profiles.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_profiles, self.ui.push_button_delete_profile))
		self.ui.list_widget_profiles.clicked.connect(lambda: self.load_profile_info(self.ui.list_widget_profiles.currentItem().data(QtCore.Qt.UserRole)))
		# self.ui.check_box_same_as_shipping.toggled.connect(self.same_as_shipping)
		# self.ui.line_edit_shipping_address.textChanged.connect(lambda: self.copy_text(self.address_pair))
		# self.ui.line_edit_shipping_address_2.textChanged.connect(lambda: self.copy_text(self.address_2_pair))
		# self.ui.line_edit_shipping_city.textChanged.connect(lambda: self.copy_text(self.city_pair))
		# self.ui.line_edit_shipping_zip.textChanged.connect(lambda: self.copy_text(self.zip_pair))
		# self.ui.combo_box_shipping_state.currentIndexChanged.connect(lambda: self.copy_index(self.state_pair))

#================================================================================
# BILLING BUTTONS
#================================================================================

		self.ui.push_button_new_billing.clicked.connect(self.new_billing_profile)
		self.ui.push_button_save_billing.clicked.connect(self.save_billing_profile)
		self.ui.push_button_delete_all_billing.clicked.connect(self.delete_all_billing_profiles)
		self.ui.push_button_delete_billing.clicked.connect(lambda: self.delete_billing_profile(self.ui.list_widget_billing.currentItem()))
		self.ui.list_widget_billing.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_billing, self.ui.push_button_delete_billing))
		self.ui.list_widget_billing.clicked.connect(lambda: self.load_billing_info(self.ui.list_widget_billing.currentItem().data(QtCore.Qt.UserRole)))

#================================================================================
# PROXY BUTTONS
#================================================================================

		self.ui.push_button_new_proxies.clicked.connect(self.new_proxy_profile)
		self.ui.push_button_import_proxies.clicked.connect(self.import_proxies)
		self.ui.push_button_save_proxies.clicked.connect(self.save_proxy_profile)
		self.ui.push_button_delete_all_proxies.clicked.connect(self.delete_all_proxy_profiles)
		self.ui.push_button_delete_proxies.clicked.connect(lambda: self.delete_proxy_profile(self.ui.list_widget_proxies.currentItem()))
		self.ui.list_widget_proxies.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_proxies, self.ui.push_button_delete_proxies))
		self.ui.plain_text_edit_proxies.textChanged.connect(self.update_proxy_count)
		self.ui.list_widget_proxies.clicked.connect(lambda: self.load_proxy_info(self.ui.list_widget_proxies.currentItem().data(QtCore.Qt.UserRole)))

#================================================================================
# ACCOUNT BUTTONS
#================================================================================

		self.ui.pb_open_login.clicked.connect(self.open_login_window)
		self.ui.pb_save_account.clicked.connect(self.save_account)

#================================================================================
# LOG BUTTONS
#================================================================================

		self.ui.push_button_export_log.clicked.connect(self.export_log)
		self.ui.push_button_clear_log.clicked.connect(self.clear_log)
		self.ui.line_edit_filter.textChanged.connect(self.filter_log)

		# Show current app version in status bar
		self.statusBar().showMessage(f'{VERSION}')

		self.ui.tabWidget.tabBar().setObjectName('tab_widget_tasks')

		self.ui.table_widget_tasks.selectionModel().selectionChanged.connect(self.select_task)

		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_tasks.horizontalHeader().setSectionsClickable(False)
		self.ui.table_widget_tasks.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_tasks.verticalHeader().setSectionsMovable(False)
		self.ui.table_widget_tasks.verticalHeader().setSectionsClickable(False)
		self.ui.table_widget_tasks.hideColumn(0)
		self.ui.table_widget_tasks.setFocusPolicy(QtCore.Qt.NoFocus)

		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.horizontalHeader().setSectionsClickable(False)
		self.ui.tw_accounts.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.verticalHeader().setSectionsMovable(True)
		self.ui.tw_accounts.verticalHeader().setSectionsClickable(False)
		self.ui.tw_accounts.setColumnHidden(0, True)
		# self.ui.table_widget_tasks.verticalHeader().setDefaultSectionSize(30)
		# self.ui.table_widget_tasks.horizontalHeader().setSectionsMovable(True)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_proxies.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		# self.ui.table_widget_proxies.horizontalHeader().setSectionsMovable(True)

		self.load_proxy_list()
		self.load_accounts()
		self.load_billing_list()
		self.load_profile_list()
		self.load_task_list()
		self.load_combo_box_profiles()
		self.load_combo_box_billing()
		self.load_combo_box_proxies()

		self.disable_mass_edit()

#================================================================================
# TOGGLE FUNCTIONS
#================================================================================

		self.toggle_button(self.ui.list_widget_profiles, self.ui.push_button_delete_profile)
		self.toggle_button(self.ui.list_widget_billing, self.ui.push_button_delete_billing)
		self.toggle_button(self.ui.list_widget_proxies, self.ui.push_button_delete_proxies)
		self.ui.group_box_options.toggled.connect(lambda: self.toggle_options(self.ui.group_box_options, self.ui.frame_options))
		self.ui.group_box_log.toggled.connect(lambda: self.toggle_log(self.ui.group_box_log, self.ui.frame_log))
		self.ui.splitter.splitterMoved.connect(self.set_splitter_sizes)

#================================================================================
# STYLE OPTIONS
#================================================================================
		# Set app style
		self.styles = Stylesheet()
		app.setStyleSheet(self.styles.dark_theme())

		self.ui.push_button_captcha.clicked.connect(self.open_captcha_window)
		self.ui.table_widget_tasks.viewport().installEventFilter(self)

		# self.ui.check_box_mask_proxies.clicked.connect(self.test)
		self.ui.check_box_mask_proxies.setCheckState(QtCore.Qt.PartiallyChecked)
		self.ui.check_box_mask_proxies.stateChanged.connect(self.toggle_mask_proxies)
		# self.ui.table_widget_tasks.selectionModel().selectionChanged.connect(self.test3)

		# # self.add_header = Testing()
		# # self.add_header.run()
		# # url = 'https://www.google.com'
		# # res = requests.get(url)
		# # print(res.headers)
		# # print('moving')
		# # ssl = QtNetwork.QSslSocket()
		# # print(ssl.sslLibraryBuildVersionString())
		# # print(ssl.supportsSsl())
		# # print(ssl.sslLibraryVersionString())
		# self.browser = QtWebEngineWidgets.QWebEngineView()
		# self.browser.loadFinished.connect(self.test)
		# self.browser.load(QtCore.QUrl('https://shop.funko.com'))
		# self.browser.show()
		# self.browser.page().loadFinished.connect(self.load_captcha_html)
		# self.interceptor = Interceptor()
		# # self.interceptor.test.connect(self.load_captcha_html)
		# # self.manager = QNetworkAccessManager()
		# # self.profile = QtWebEngineWidgets.QWebEngineProfile()
		# self.browser.page().profile().setUrlRequestInterceptor(self.interceptor)
		# # self.browser.setContent(bytes(html, 'utf-8'), 'text/html', QtCore.QUrl('https://shop.funko.com'))
		# # self.browser.show()
		# # self.request = QtNetwork.QNetworkRequest()
		# # self.config = self.request.sslConfiguration()
		# # self.config.setProtocol(QtNetwork.QSsl.AnyProtocol)
		# # self.request.setSslConfiguration(self.config)
		# # self.request.setUrl(QtCore.QUrl('http://shop.funko.com/'))
		# # self.r = self.manager.get(self.request)
		# # self.r = self.manager.head(self.request)
		# # self.r.finished.connect(self.test)
		# # self.browser.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
		# # self.channel = QtWebChannel.QWebChannel(self.browser.page())
		# # self.page.setHtml(html)
		# # self.headers = QtWebEngineCore.QWebEngineHttpRequest(QtCore.QUrl('https://shop.funko.com'))
		# # self.browser.load(self.headers)
		# # print(self.headers.headers())
		# self.browser.load(QtCore.QUrl('https://shop.funko.com'))
		# # self.browser.load(QtCore.QUrl.fromLocalFile('/recaptcha.html'))
		# # self.browser.load(QtCore.QUrl.fromLocalFile(QtCore.QFileInfo('test.html').absoluteFilePath()))
		# # self.page.setUrl(QtCore.QUrl('https://www.google.com/recaptcha/api2/demo'))
		# self.browser.resize(400, 620)
		# self.browser.show()

		self.q_proxy = QNetworkProxy()
		self.q_proxy.setType(QNetworkProxy.HttpProxy)
		self.q_proxy.setHostName('154.37.109.192')
		self.q_proxy.setPort(17102)
		self.q_proxy.setUser('napupr')
		self.q_proxy.setPassword('lagtvf')

		# self.render_view = QtWebEngineWidgets.QWebEnginePage()
		# self.start = time.time()
		# self.render_view.load(QtCore.QUrl('https://colourpop.com'))
		# self.render_view.loadFinished.connect(self.test)

		# MainWindow.show()
		# exit = app.exec_()
		# # Code to run before exit
		# self.export_main_log()
		# sys.exit(exit)

		# Center the app
		self.center()

		self.s = requests.Session()

		self.headers = {
			'accept': 'application/json',
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
		}

		self.sku = '5723316'
		self.cart_id = None
		self.line_id = None
		self.token = None
		self.redirect_url = None
		self.order_id = None
		self.threeDS = None

		# self.ui.pb_login.clicked.connect(self.login)
		# self.ui.pb_step_1.clicked.connect(self.add_to_cart)
		# self.ui.pb_step_2.clicked.connect(self.get_basket)
		# self.ui.pb_step_3.clicked.connect(self.checkout)
		# self.ui.pb_step_4.clicked.connect(self.sign_in_as_guest)
		# self.ui.pb_step_5.clicked.connect(self.patch_item_info)
		# self.ui.pb_step_6.clicked.connect(self.patch_guest_info)
		# self.ui.pb_step_7.clicked.connect(self.load_browser)

#================================================================================
# ACCOUNT FUNCTIONS
#================================================================================

	def load_accounts(self):
		self.ui.tw_accounts.setRowCount(0)
		data = self.tgadb.get_all_accounts()
		if data:
			self.create_account(data)
		else:
			print('No accounts')

	def create_account(self, data):
		for a, b, c, d in data:
			account = Account(a, b, c, d)
			# account.update_cookies.connect(self.update_account)
			account.delete_account.connect(self.delete_account)
			self.add_account(account)
			self.accounts[a] = account
			self.ui.combo_box_accounts.addItem(b, a)

	def add_account(self, account):
		row = self.ui.tw_accounts.rowCount()
		self.ui.tw_accounts.insertRow(row)
		self.ui.tw_accounts.setItem(row, 0, account.w_account_id)
		self.ui.tw_accounts.setItem(row, 1, account.w_account_name)
		self.ui.tw_accounts.setItem(row, 2, account.w_account_store)
		self.ui.tw_accounts.setCellWidget(row, 3, account.w_actions)

	def delete_account(self, account_id):
		self.tgadb.delete_account(account_id)
		self.ui.tw_accounts.clearContents()
		self.load_accounts()

	def update_account(self, key, value, account_id):
		self.tgadb.update_account(key, value, account_id)

	def save_account(self):
		items = {}
		items['account_name'] = self.ui.le_account_name.text()
		items['account_store'] = self.ui.cb_login_store.currentText()
		cookie_dict = {}
		cookie_list = self.cookie_jar.allCookies()
		for cookie in cookie_list:
			index = cookie_list.index(cookie)
			name = cookie.name().data().decode()
			value = cookie.value().data().decode()
			domain = cookie.domain()
			path = cookie.path()
			expire = cookie.expirationDate().toString()
			cookie_dict[index] = {
				'name': name,
				'value': value,
				'domain': domain,
				'path': path,
				'expire': expire
			}
		items['account_cookies'] = json.dumps(cookie_dict)
		self.tgadb.save_account(items)
		data = self.tgadb.get_recent_account()
		self.create_account(data)

	def open_login_window(self):
		# self.cookies = []
		self.cookie_jar = QNetworkCookieJar()
		self.login_window = QtWebEngineWidgets.QWebEngineView()
		# url = self.ui.cb_login_store.currentText()
		# self.domain = url.split('/')[-2].split('.')[-2]
		url = 'https://gsp.target.com/gsp/authentications/v1/auth_codes?client_id=ecom-web-1.0.0&state=1585456116676&redirect_uri=https://www.target.com/&assurance_level=M'
		self.login_window.load(QtCore.QUrl(url))
		self.login_window.page().profile().cookieStore().deleteAllCookies()
		self.cookie_store = self.login_window.page().profile().cookieStore()
		self.cookie_store.cookieAdded.connect(self.on_cookie_added)
		self.login_window.show()

	def on_cookie_added(self, cookie):
		self.cookie_jar.insertCookie(cookie)

#================================================================================
# TEST FUNCTIONS
#================================================================================

	def add_to_cart(self):
		print('Adding to cart')
		url = 'https://www.bestbuy.com/cart/api/v1/addToCart'
		payload = {
			'items': [{
				'skuId': self.sku
			}]
		}
		r = self.s.post(url, headers=self.headers, json=payload)
		print(r)
		data = r.json()
		self.line_id = data['summaryItems'][0]['lineId']
		print(data)

	def get_basket(self):
		print('Getting basket')
		# Get cart id
		url = 'https://www.bestbuy.com/basket/v1/basket'
		h = self.headers
		h['X-CLIENT-ID'] = 'not null'
		r = self.s.get(url, headers=h)
		print(r)
		data = r.json()
		print(data)
		self.cart_id = data['id']

	def checkout(self):
		print('Selecting shipping')
		url = f'https://www.bestbuy.com/cart/item/{self.line_id}/fulfillment'
		h = self.headers
		h['X-ORDER-ID'] = self.cart_id
		payload = {
			'selected': 'SHIPPING'
		}
		r = self.s.put(url, headers=h, json=payload)
		print(r)
		data = r.json()
		print(data)

		print('Starting checkout')
		url = 'https://www.bestbuy.com/cart/d/checkout'
		h = self.headers
		h['X-ORDER-ID'] = self.cart_id
		payload = {}
		r = self.s.post(url, headers=h, json=payload)
		print(r)
		data = r.json()
		print(data)
		self.token = data['updateData']['order']['ciaToken']
		print(self.token)

	def sign_in_as_guest(self):
		print('Signing in as guest')
		url = 'https://www.bestbuy.com/identity/guest'
		params = {
			'token': self.token
		}
		r = self.s.get(url, headers=self.headers, params=params)
		print(r)

	def patch_item_info(self):
		print('Patching item info')
		url = f'https://www.bestbuy.com/checkout/orders/{self.cart_id}/'
		h = self.headers
		h['X-User-Interface'] = 'DotCom-Optimized'
		payload = {
			'items': [{
				'id': self.line_id,
				'giftMessageSelected': False,
				'type': 'DEFAULT',
				'selectedFulfillment': {
					'shipping': {
						'address': {
							'city': 'Atlanta',
							'country': 'US',
							'dayPhoneNumber': '4709914999',
							'firstName': 'James',
							'isWishListAddress': False,
							'lastName': 'Han',
							'middleInitial': '',
							'override': False,
							'saveToProfile': False,
							'state': 'GA',
							'street': '2850 Arrow Creek Dr',
							'street2': '',
							'type': 'RESIDENTIAL',
							'useAddressAsBilling': False,
							'zipcode': '30341'
						}
					}
				}
			}]
		}
		r = self.s.patch(url, headers=h, json=payload)
		print(r)
		data = r.json()
		print(data)

	def patch_guest_info(self):
		print('Patching guest info')
		url = f'https://www.bestbuy.com/checkout/orders/{self.cart_id}/'
		h = self.headers
		h['X-User-Interface'] = 'DotCom-Optimized'
		payload = {
			'emailAddress': 'semajhan@gmail.com',
			'phoneNumber': '7737081444',
			'smsNotifyNumber': '',
			'smsOptIn': False
		}
		r = self.s.patch(url, headers=h, json=payload)
		print(r)
		self.url = r.url
		data = r.json()
		print(data)
		self.order_id = data['customerOrderId']

	def load_browser(self):
		self.view = QWebEngineView()
		for cookie in self.s.cookies:
			c = QtNetwork.QNetworkCookie()
			c.setDomain(cookie.__dict__['domain'])
			c.setName(bytes(cookie.__dict__['name'], 'utf-8'))
			c.setValue(bytes(cookie.__dict__['value'], 'utf-8'))
			self.view.page().profile().cookieStore().setCookie(c)

		url = 'https://www.bestbuy.com/pricing/v1/price/item?salesChannel=LargeView&visitorId=69ce0719-703c-11ea-bcf3-124957b72707&context=CHECKOUT&catalog=BBY&skuId=5723316&usePriceWithCart=true&cartTimestamp=1585776484898'
		self.view.load(QtCore.QUrl('https://www.bestbuy.com/checkout/r/payment'))
		self.view.loadFinished.connect(self.to_html)
		self.view.show()

	def to_html(self):
		self.view.page().toHtml(self.call)

	def call(self, html):
		# print(html)
		script = '''
		document.getElementById('optimized-cc-card-number').focus();
		document.getElementById('optimized-cc-card-number').value = '4833130037628039';
		'''
		self.view.page().runJavaScript(script)

	# def login(self):
	# 	self.cookies = []
	# 	self.view = QtWebEngineWidgets.QWebEngineView()
	# 	url = 'https://login.target.com/gsp/static/v1/login/'
	# 	# self.request = QWebEngineHttpRequest(QtCore.QUrl(url))
	# 	self.view.load(QtCore.QUrl(url))
	# 	# self.view.loadFinished.connect(self.print_html)
	# 	self.view.page().profile().cookieStore().deleteAllCookies()
	# 	self.cookie_store = self.view.page().profile().cookieStore()
	# 	self.cookie_store.cookieAdded.connect(self.on_cookie_added)
	# 	self.view.show()

	# def on_cookie_added(self, cookie):
	# 	for c in self.cookies:
	# 		if c.hasSameIdentifier(cookie):
	# 			return
	# 	# self.cookies.append(QNetworkCookie(cookie))
	# 	nc = QNetworkCookie(cookie)
	# 	name = nc.name().data().decode()
	# 	value = nc.value().data().decode()
	# 	self.s.cookies.set(name, value, domain=nc.domain())

	def test_shopify(self):
		self.shopify = gecko_utils.check_shopify_api_key(self.ui.line_edit_custom_shopify.text())
		self.ui.label_tested.setText(self.shopify['status'])
		print(self.shopify)

	# def test(self):
	# 	self.render_view.toHtml(self.lol)

	def lol(self, data):
		print(data)
		end = time.time()
		dif = round(end - self.start, 2)
		print('[TIME]: {}'.format(dif))

	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def send_token(self, task_id, token):
		self.tasks[task_id].token = token

	# def get_token_from_queue(self, task_id, store):
	# 	try:
	# 		token = self.tokens[store].get(block=False)
	# 	except queue.Empty:
	# 		token = None

	# 	if token:
	# 		self.tasks[task_id].token = token

	def copy_text(self, pair):
		if self.ui.check_box_same_as_shipping.isChecked():
			pair[1].setText(pair[0].text())

	def copy_index(self, pair):
		if self.ui.check_box_same_as_shipping.isChecked():
			pair[1].setCurrentIndex(pair[0].currentIndex())

	def request_captcha(self, task_id):
		self.tasks[task_id].load_captcha()

	def poll_response(self, task_id):
		self.tasks[task_id].check_response()

	# def request_captcha(self, task_id, url, cookies):
	# 	if not self.captcha_window.load_captcha(task_id, url):
	# 		self.tasks[task_id].solver_available = False

	def avail(self):
		self.captcha_window.avail()

	def unavail(self):
		self.captcha_window.unavail()

	def test(self):
		self.tasks[self.task_ids[0]].store.test()

	def test2(self):
		self.captcha_window.test('https://shop.funko.com')

	def test3(self, selected, deselected):
		print(self.ui.table_widget_tasks.selectedIndexes()[0::9])
		# for i in self.ui.table_widget_tasks.selectedIndexes()[0::9]:
		# 	print()
		# print(self.ui.table_widget_tasks.selectionModel())

	def toggle_button(self, item, button):
		if type(item) is QtWidgets.QListWidget:
			if item.selectedItems():
				button.setEnabled(True)
			else:
				button.setEnabled(False)
		else:
			print('Item {} not supported'.format(type(item)))

#================================================================================
# MOUSE FUNCTIONS
#================================================================================

# Nothing as of yet, may implement later

#================================================================================
# TOGGLE FUNCTIONS
#================================================================================

	def toggle_cbe_task_type(self):
		if self.ui.cbe_task_type.isChecked():
			self.ui.label_task_type.setEnabled(True)
			self.ui.combo_box_task_type.setEnabled(True)
		else:
			self.ui.label_task_type.setEnabled(False)
			self.ui.combo_box_task_type.setEnabled(False)

	def toggle_cbe_store(self):
		if self.ui.cbe_store.isChecked():
			self.ui.label_store.setEnabled(True)
			self.ui.combo_box_store.setEnabled(True)
		else:
			self.ui.label_store.setEnabled(False)
			self.ui.combo_box_store.setEnabled(False)

	def toggle_cbe_search_type(self):
		if self.ui.cbe_search_type.isChecked():
			self.ui.label_search_type.setEnabled(True)
			self.ui.combo_box_search_type.setEnabled(True)
		else:
			self.ui.label_search_type.setEnabled(False)
			self.ui.combo_box_search_type.setEnabled(False)

	def toggle_cbe_search(self):
		if self.ui.cbe_search.isChecked():
			self.ui.label_search.setEnabled(True)
			self.ui.line_edit_search.setEnabled(True)
		else:
			self.ui.label_search.setEnabled(False)
			self.ui.line_edit_search.setEnabled(False)

	def toggle_cbe_task_name(self):
		if self.ui.cbe_task_name.isChecked():
			self.ui.label_task_name.setEnabled(True)
			self.ui.line_edit_task_name.setEnabled(True)
		else:
			self.ui.label_task_name.setEnabled(False)
			self.ui.line_edit_task_name.setEnabled(False)

	def toggle_cbe_qty(self):
		if self.ui.cbe_qty.isChecked():
			self.ui.label_qty.setEnabled(True)
			self.ui.combo_box_qty.setEnabled(True)
		else:
			self.ui.label_qty.setEnabled(False)
			self.ui.combo_box_qty.setEnabled(False)

	def toggle_cbe_account(self):
		if self.ui.cbe_account.isChecked():
			self.ui.check_box_account.setEnabled(True)
		else:
			self.ui.check_box_account.setEnabled(False)

		self.ui.check_box_account.setChecked(False)
		self.toggle_accounts()

	def toggle_cbe_profile(self):
		if self.ui.cbe_profile.isChecked():
			self.ui.label_profile.setEnabled(True)
			self.ui.combo_box_profile.setEnabled(True)
		else:
			self.ui.label_profile.setEnabled(False)
			self.ui.combo_box_profile.setEnabled(False)

	def toggle_cbe_billing(self):
		if self.ui.cbe_billing.isChecked():
			self.ui.label_billing.setEnabled(True)
			self.ui.combo_box_billing.setEnabled(True)
		else:
			self.ui.label_billing.setEnabled(False)
			self.ui.combo_box_billing.setEnabled(False)

	def toggle_cbe_proxies(self):
		if self.ui.cbe_proxies.isChecked():
			self.ui.check_box_proxies.setEnabled(True)
		else:
			self.ui.check_box_proxies.setEnabled(False)

		self.ui.check_box_proxies.setChecked(False)
		self.toggle_proxies()

	def toggle_cbe_rotation(self):
		if self.ui.cbe_rotation.isChecked():
			self.ui.label_rotation.setEnabled(True)
			self.ui.combo_box_rotation.setEnabled(True)
		else:
			self.ui.label_rotation.setEnabled(False)
			self.ui.combo_box_rotation.setEnabled(False)

	def toggle_cbe_size(self):
		if self.ui.cbe_size.isChecked():
			self.ui.check_box_size.setEnabled(True)
		else:
			self.ui.check_box_size.setEnabled(False)

		self.ui.check_box_size.setChecked(False)
		self.toggle_size()

	def toggle_cbe_color(self):
		if self.ui.cbe_color.isChecked():
			self.ui.check_box_color.setEnabled(True)
		else:
			self.ui.check_box_color.setEnabled(False)

		self.ui.check_box_color.setChecked(False)
		self.toggle_color()

	def toggle_cbe_category(self):
		if self.ui.cbe_category.isChecked():
			self.ui.check_box_category.setEnabled(True)
		else:
			self.ui.check_box_category.setEnabled(False)

		self.ui.check_box_category.setChecked(False)
		self.toggle_category()

	def toggle_cbe_price_range(self):
		if self.ui.cbe_price_range.isChecked():
			self.ui.check_box_price_range.setEnabled(True)
		else:
			self.ui.check_box_price_range.setEnabled(False)

		self.ui.check_box_price_range.setChecked(False)
		self.toggle_price_range()

	def toggle_cbe_delay_range(self):
		if self.ui.cbe_delay_range.isChecked():
			self.ui.label_delay_range.setEnabled(True)
			self.ui.line_edit_delay_min.setEnabled(True)
			self.ui.line_edit_delay_max.setEnabled(True)
		else:
			self.ui.label_delay_range.setEnabled(False)
			self.ui.line_edit_delay_min.setEnabled(False)
			self.ui.line_edit_delay_max.setEnabled(False)

	def toggle_cbe_captcha(self):
		if self.ui.cbe_captcha.isChecked():
			self.ui.check_box_captcha.setEnabled(True)
		else:
			self.ui.check_box_captcha.setEnabled(False)

		self.ui.check_box_captcha.setChecked(False)

	def toggle_accounts(self):
		self.ui.combo_box_account.clear()
		if self.ui.cbe_account.isChecked():
			if self.ui.check_box_account.isChecked():
				self.ui.combo_box_account.setEnabled(True)
				self.ui.combo_box_account.setCurrentIndex(-1)
			else:
				self.ui.combo_box_account.setEnabled(False)
				self.ui.combo_box_account.addItem('N/A')
		else:
			self.ui.combo_box_account.setEnabled(False)

	def toggle_proxies(self):
		self.ui.combo_box_proxies.clear()
		if self.ui.cbe_proxies.isChecked():
			if self.ui.check_box_proxies.isChecked():
				self.ui.combo_box_proxies.setEnabled(True)
				self.load_combo_box_proxies()
				self.ui.combo_box_proxies.setCurrentIndex(0)
			else:
				self.ui.combo_box_proxies.setEnabled(False)
				self.ui.combo_box_proxies.addItem('localhost')
		else:
			self.ui.combo_box_proxies.setEnabled(False)

	def toggle_size(self):
		self.ui.combo_box_size.clear()
		if self.ui.cbe_size.isChecked():
			if self.ui.check_box_size.isChecked():
				self.ui.combo_box_size.setEnabled(True)
				self.load_combo_box_sizes()
				self.ui.combo_box_size.setCurrentIndex(0)
			else:
				self.ui.combo_box_size.setEnabled(False)
				self.ui.combo_box_size.addItem('Any')
		else:
			self.ui.combo_box_size.setEnabled(False)

	def toggle_color(self):
		self.ui.line_edit_color.clear()
		if self.ui.cbe_color.isChecked():
			if self.ui.check_box_color.isChecked():
				self.ui.line_edit_color.setEnabled(True)
			else:
				self.ui.line_edit_color.setEnabled(False)
				self.ui.line_edit_color.setText('Any')
		else:
			self.ui.line_edit_color.setEnabled(False)

	def toggle_category(self):
		self.ui.combo_box_category.clear()
		if self.ui.cbe_category.isChecked():
			if self.ui.check_box_category.isChecked():
				self.ui.combo_box_category.setEnabled(True)
				self.load_combo_box_categories()
				self.ui.combo_box_category.setCurrentIndex(0)
			else:
				self.ui.combo_box_category.setEnabled(False)
				self.ui.combo_box_category.addItem('Any')
		else:
			self.ui.combo_box_category.setEnabled(False)

	def toggle_price_range(self):
		self.ui.line_edit_price_min.clear()
		self.ui.line_edit_price_max.clear()
		if self.ui.cbe_price_range.isChecked():
			if self.ui.check_box_price_range.isChecked():
				self.ui.line_edit_price_min.setEnabled(True)
				self.ui.line_edit_price_max.setEnabled(True)
			else:
				self.ui.line_edit_price_min.setEnabled(False)
				self.ui.line_edit_price_max.setEnabled(False)
		else:
			self.ui.line_edit_price_min.setEnabled(False)
			self.ui.line_edit_price_max.setEnabled(False)

	def toggle_mask_proxies(self):
		for task in self.tasks.values():
			task.check_box_mask_proxy.setCheckState(self.ui.check_box_mask_proxies.checkState())
			# task.mask_proxies(self.ui.check_box_mask_proxies.checkState())
		self.ui.table_widget_tasks.resizeColumnToContents(7)

#================================================================================
# CAPTCHA FUNCTIONS
#================================================================================

	def open_captcha_window(self):
		self.captcha_window.show()
		self.captcha_window.activateWindow() # Bring window to front

	# def open_captcha_window(self):
	# 	data = self.tgadb.get_all_solvers()
	# 	if data:
	# 		i = 1
	# 		for a, b in data:
	# 			solver = Solver(a, b)
	# 			solver.solver_name = 'Solver ({})'.format(i)
	# 			solver.request_token.connect(self.get_token)
	# 			solver.request_element.connect(self.get_element)
	# 			solver.add_token.connect(self.save_token)
	# 			self.solvers[a] = solver
	# 			self.solver_window.add_solver(solver)
	# 			i += 1
	# 	else:
	# 		self.save_solver()
	# 	self.solver_window.show()

	# def save_solver(self):
	# 	items = {
	# 		'solver_name': 'Solver'
	# 	}
	# 	try:
	# 		self.tgadb.save_solver(items)
	# 	except Exception as e:
	# 		print(str(e))

	# 	data = self.tgadb.get_recent_solver()
	# 	for a, b in data:
	# 		solver = Solver(a, b)
	# 		solver.check_for_result.connect(self.check_for_result)
	# 		self.solvers[a] = solver
	# 		self.solver_window.add_solver(solver)

	# def start_solver(self, solver_id):
	# 	self.solvers[solver_id].start()

	# def delete_solver(self, solver_id):
	# 	self.solvers[solver_id].stop_solver()
	# 	del self.solvers[solver_id]
	# 	try:
	# 		self.tgadb.delete_solver(solver_id)
	# 	except Exception as e:
	# 		print(str(e))

	# def stop_solvers(self):
	# 	print('stopping')
	# 	for solver in self.solvers.values():
	# 		solver.stop_solver()

	# def get_element(self, solver_id):
	# 	self.solvers[solver_id].get_element()

	# def get_token(self, solver_id):
	# 	self.solvers[solver_id].get_token()
	# 	# self.solvers[solver_id].test()
	# 	# self.solvers[solver_id].solver.page().runJavaScript("document.getElementById('g-recaptcha-response').value;", self.print_captcha)

	# def save_token(self, store_name, value):
	# 	self.queues[store_name].q.put(value)

	# def send_to_available_solver(self, store_name, cookies, sitekey):
	# 	print(len(self.solvers))
	# 	if len(self.solvers) > 0:
	# 		for solver in self.solvers.values():
	# 			if solver.available:
	# 				solver.store_name = store_name
	# 				solver.sitekey = sitekey
	# 				solver.solver.set_cookies(cookies)
	# 				# solver.load_captcha(self.stores[store_name])
	# 				# solver.load_page('https://shop.funko.com/')
	# 				solver.load_page('https://www.supremenewyork.com/')
	# 				break
	# 				# self.tasks[task_id].solver_id = solver.solver_id

	# def poll_token(self, task_id, store_name):
	# 	self.tasks[task_id].token = self.queues[store_name].get_token()

#================================================================================
# SIGNAL FUNCTIONS
#================================================================================

	def update_task_title(self, task_id):
		self.tasks[task_id].set_title()
		# row = self.ui.table_widget_tasks.row(item)
		# self.ui.table_widget_tasks.item(row, 4).setText(title)

	def update_task_image(self, task_id):
		self.tasks[task_id].set_image()
		self.ui.table_widget_tasks.resizeColumnToContents(5)

	def update_task_size(self, task_id):
		self.tasks[task_id].set_size()
		self.ui.table_widget_tasks.resizeColumnToContents(6)

	def update_task_proxy(self, task_id):
		self.tasks[task_id].set_proxy()

	def update_task_delay(self, task_id):
		self.tasks[task_id].set_delay()

	def update_task_status(self, task_id):
		self.tasks[task_id].set_status()
		# row = self.ui.table_widget_tasks.row(item)
		# self.ui.table_widget_tasks.item(row, 8).setText(message)
		# self.ui.table_widget_tasks.resizeColumnToContents(8)

	def update_task_run(self, task_id):
		self.tasks[task_id].set_run()

	def update_task_sleep(self, task_id):
		self.tasks[task_id].set_sleep()

	def update_task_log(self, message):
		self.post_to_log(message)

#================================================================================
# CORE FUNCTIONS
#================================================================================

	def select_task(self):
		self.task_ids = []
		data = self.ui.table_widget_tasks.selectionModel().selectedIndexes()[::9]
		for i in data:
			task_id = i.data((QtCore.Qt.UserRole))
			self.task_ids.append(task_id)

		task_count = len(self.task_ids)

		self.disable_mass_edit()
		if task_count == 1:
			# Single row selected
			self.load_task_info(self.task_ids[0])
		elif task_count > 1:
			# Multiple row selected
			self.enable_mass_edit()
		else:
			# No row selected
			self.new_task()

	def load_stores(self, task_type):
		self.ui.combo_box_store.clear()
		for store in self.stores:
			for key, value in store['task_type'].items():
				if task_type == key and value:
					self.ui.combo_box_store.addItem(store['url'])

	def load_search_options(self, store_type):
		self.ui.combo_box_search_type.clear()
		for store in self.stores:
			if store_type == store['url']:
				for key, value in store['search_type'].items():
					if value:
						self.ui.combo_box_search_type.addItem(key)
				
				break

	def load_task_options(self, search_type):
		print(f'Search type is: {search_type}')

	# def load_types(self, index):
	# 	self.ui.combo_box_search_type.clear()
	# 	self.ui.combo_box_task_type.clear()
	# 	data = self.ui.combo_box_store.currentData(QtCore.Qt.UserRole)
	# 	if data:
	# 		# Search type
	# 		if 'k' in data:
	# 			self.ui.combo_box_search_type.addItem('Keywords')
	# 		if 'd' in data:
	# 			self.ui.combo_box_search_type.addItem('Direct Link')
	# 		if 'v' in data:
	# 			self.ui.combo_box_search_type.addItem('Variant')
	# 		# Task type
	# 		if 'n' in data:
	# 			self.ui.combo_box_task_type.addItem('Normal')
	# 		if 'm' in data:
	# 			self.ui.combo_box_task_type.addItem('Monitor')
	# 		if 'r' in data:
	# 			self.ui.combo_box_task_type.addItem('Restock')

	def closeEvent(self, event):
		self.captcha_window.close()
		# self.solver_window.close()
		# self.local_server.stop()
		# self.add_header.stop()
		# for server in self.servers.values():
		# 	server.stop()

	def set_splitter_sizes(self):
		# self.ui.splitter.setSizes(self.ui.splitter.sizes())
		self.old_sizes = self.ui.splitter.sizes()

	def toggle_options(self, group_box, frame):
		if group_box.isChecked():
			frame.show()
			sizes = self.old_sizes
			sizes[2] = self.ui.splitter.sizes()[2]
			self.ui.splitter.setSizes(sizes)
		else:
			self.old_sizes = self.ui.splitter.sizes()
			frame.hide()
			sizes = [16, self.old_sizes[1] + (self.old_sizes[0] - 16), self.ui.splitter.sizes()[2]]
			self.ui.splitter.setSizes(sizes)

	def toggle_log(self, group_box, frame):
		if group_box.isChecked():
			frame.show()
			sizes = self.old_sizes
			sizes[0] = self.ui.splitter.sizes()[0]
			self.ui.splitter.setSizes(sizes)
		else:
			self.old_sizes = self.ui.splitter.sizes()
			frame.hide()
			sizes = [self.ui.splitter.sizes()[0], self.old_sizes[1] + (self.old_sizes[2] - 16), 16]
			self.ui.splitter.setSizes(sizes)

	def validate_fields(self, fields, t='all'):
		self.mass_edit_fields = {}
		if t == 'num': 
			for item in fields:
				if item.isEnabled():
					if self.is_empty(item):
						return False
					if not self.is_number(item.text()):
						return False
			return True
		elif t == 'any':
			for item in fields:
				if item.isEnabled():
					if self.is_empty(item):
						return False
			return True
		elif t == 'all':
			for item in fields:
				if item.isEnabled():
					if self.is_empty(item):
						return False
					else:
						if type(item) is QtWidgets.QComboBox:
							self.mass_edit_fields[item.objectName()] = item.currentText()
						elif type(item) is QtWidgets.QLineEdit:
							self.mass_edit_fields[item.objectName()] = item.text()
						elif type(item) is QtWidgets.QCheckBox:
							self.mass_edit_fields[item.objectName()] = item.checkState()
						else:
							print('Not a QComboBox, QLineEdit, or QCheckBox')
			return True
		else:
			print('{} does not match t'.format(t))

	def check_mass_edit_fields(self):
		mass_edit_fields = {}
		for item in self.task_fields:
			if item.isEnabled():
				if self.is_empty(item):
					return False
				else:
					if type(item) is QtWidgets.QComboBox:
						if item.objectName() == 'combo_box_profiles':
							mass_edit_fields[item.objectName()] = item.currentData(QtCore.Qt.UserRole)
						elif item.objectName() == 'combo_box_billing':
							mass_edit_fields[item.objectName()] = item.currentData(QtCore.Qt.UserRole)
						elif item.objectName() == 'combo_box_proxies':
							mass_edit_fields[item.objectName()] = item.currentData(QtCore.Qt.UserRole)
						else:
							mass_edit_fields[item.objectName()] = item.currentText()
					elif type(item) is QtWidgets.QLineEdit:
						mass_edit_fields[item.objectName()] = item.text()
					elif type(item) is QtWidgets.QComboBox:
						mass_edit_fields[item.objectName()] = item.currentText()
		return mass_edit_fields

	def is_number(self, item):
		for char in item:
			if char not in '1234567890':
				return False
		return True

	def is_empty(self, item):
		if type(item) is QtWidgets.QLineEdit:
			if len(item.text()) > 0:
				return False
		elif type(item) is QtWidgets.QComboBox:
			if len(item.currentText()) > 0:
				return False
		elif type(item) is QtWidgets.QPlainTextEdit:
			if len(item.toPlainText()) > 0:
				return False
		elif type(item) is QtWidgets.QCheckBox:
			return False
		return True

	def permission_dialog(self, title, message):
		ok = QtWidgets.QMessageBox.Ok
		cancel = QtWidgets.QMessageBox.Cancel
		d = QtWidgets.QMessageBox()
		d.setWindowTitle(title)
		d.setText(message)
		d.setStandardButtons(ok | cancel)
		d.exec_()
		if d.result() == ok:
			return True
		else:
			return False

	def confirmation_dialog(self, title, message):
		yes = QtWidgets.QMessageBox.Yes
		cancel = QtWidgets.QMessageBox.Cancel
		d = QtWidgets.QMessageBox()
		d.setWindowTitle(title)
		d.setText(message)
		d.setStandardButtons(yes | cancel)
		d.exec_()
		if d.result() == yes:
			return True
		else:
			return False

	def update_delay_label(self, label, base, var):
		delay = 0
		variance = 0
		if not self.is_empty(base):
			if self.is_number(base.text()):
				delay = self.convert_to_number(base.text())

		if not self.is_empty(var):
			if self.is_number(var.text()):
				variance = self.convert_to_number(var.text())

		delay_start_range = delay - variance
		delay_end_range = delay + variance
		if delay == 0:
			label.setText('')
		else:
			if variance == 0:
				label.setText('{} ms'.format(delay))
			else:
				if delay_start_range < 0:
					delay_start_range = 0

				label.setText('{} - {} ms'.format(delay_start_range, delay_end_range))

	def convert_to_number(self, item):
		return int(item)

#================================================================================
# GROUP BOX TASK FUNCTIONS
#================================================================================

	def start_tasks(self):
		if len(self.task_ids) > 0:
			for task_id in self.task_ids:
				self.tasks[task_id].start_task()
				self.tasks[task_id].enable_stop()
		else:
			for task in self.tasks.values():
				task.start_task()
				task.enable_stop()

	def stop_tasks(self):
		if len(self.task_ids) > 0:
			for task_id in self.task_ids:
				self.tasks[task_id].stop_task()
				self.tasks[task_id].enable_start()
		else:
			for task in self.tasks.values():
				task.stop_task()
				task.enable_start()

	def delete_all_tasks(self):
		if self.confirmation_dialog('Please Confirm', 'Are you sure you want to delete all tasks?'):
			self.tgadb.delete_all_tasks()
			self.ui.table_widget_tasks.setRowCount(0)
			self.post_to_log('Deleted all tasks successfully')

	def open_captcha(self):
		pass

#================================================================================
# GROUP BOX LOG FUNCTIONS
#================================================================================

	def filter_log(self):
		pass
		# search = self.ui.line_edit_filter.text()
		# original_copy = 
		# if len(search) > 0:
		# 	for line in self.ui.plainTextEdit.toPlainText().split('\n'):
		# 		if search in line:
		# 			self.ui.plainTextEdit.appendPlainText()
		# 	log_text = self.ui.plainTextEdit.toPlainText()

	def clear_log(self):
		self.ui.plainTextEdit.clear()

	def export_log(self):
		x = self.current_datetime()
		output = "{}-{}-{} {}-{}-{}.txt".format(x.strftime('%m'), x.strftime('%d'), x.strftime('%Y'), x.strftime('%H'), x.strftime('%M'), x.strftime('%S'))
		# output = x.strftime("%m") + "-" + x.strftime("%d") + "-" + x.strftime("%Y") + " " + x.strftime("%H") + "-" + x.strftime("%M") + "-" + x.strftime("%S") + ".txt"
		try:
			with open(output, mode='w') as f:
				f.write(self.ui.plainTextEdit.toPlainText())
		except Exception as e:
			self.ui.plainTextEdit.appendPlainText('[{}] Error exporting to file: {}'.format(self.current_datetime(), str(e)))
		else:
			self.ui.plainTextEdit.appendPlainText('[{}] Successfully exported as {}'.format(self.current_datetime(), output))

	def export_main_log(self):
		try:
			with open('main.txt', mode='a') as f:
				f.write('{}\n'.format(self.ui.plainTextEdit.toPlainText()))
		except Exception as e:
			print(str(e))
		else:
			print('Success')

	def current_datetime(self):
		return datetime.datetime.now()

	def post_to_log(self, message):
		self.ui.plainTextEdit.appendPlainText('[{}] {}'.format(self.current_datetime(), message))

#================================================================================
# TASK PAGE
#================================================================================

	def load_task_list(self):
		self.create_task(self.tgadb.get_all_tasks())

	def create_task(self, task_data):
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa in task_data:
			account = self.accounts[j] if j else None
			profile = self.profiles[k] if k else None
			billing = self.billing[l] if l else None
			proxies = self.proxies[n] if n else None
			task = Task(
				task_id=a,
				task_type=b,
				store_name=c,
				custom_store=d,
				search_type=e,
				search=f,
				task_name=g,
				qty=h,
				check_box_account=i,
				account=account,
				profile=profile,
				billing=billing,
				check_box_proxies=m,
				proxies=proxies,
				rotation=o,
				check_box_size=p,
				size=q,
				check_box_color=r,
				color=s,
				check_box_category=t,
				category=u,
				check_box_price_range=v,
				price_min=w,
				price_max=x,
				delay_min=y,
				delay_max=z,
				check_box_captcha=aa
			)
			task.update_log.connect(self.update_task_log)
			task.button_start.clicked.connect(task.start_task)
			task.button_stop.clicked.connect(task.stop_task)
			task.button_delete.clicked.connect(task.delete_task)
			# task.button_account.clicked.connect(task.store.account_login)
			task.started.connect(task.enable_stop)
			task.finished.connect(task.enable_start)
			task.delete.connect(self.delete_task)
			task.error_delete.connect(self.error_on_delete_task)
			task.request_captcha.connect(self.request_captcha)
			task.poll_response.connect(self.poll_response)
			task.request_abort.connect(self.request_abort)
			task.update_proxy_label.connect(self.update_proxy)
			task.load_browser.connect(self.load_task_browser)
			task.update_title.connect(self.update_task_title)
			task.update_image.connect(self.update_task_image)
			task.update_size.connect(self.update_task_size)
			task.update_proxy.connect(self.update_task_proxy)
			# task.update_delay.connect(self.update_task_delay)
			task.update_status.connect(self.update_task_status)
			task.update_run.connect(self.update_task_run)

			if task.task_id in self.tasks.keys():
				row = self.ui.table_widget_tasks.row(self.tasks[task.task_id].widget_task_id)
			else:
				row = self.ui.table_widget_tasks.rowCount()
				self.ui.table_widget_tasks.insertRow(row)

			self.ui.table_widget_tasks.setItem(row, 0, task.widget_task_id)
			self.ui.table_widget_tasks.setCellWidget(row, 1, task.widget_task_type)
			self.ui.table_widget_tasks.setCellWidget(row, 2, task.widget_name_store)
			self.ui.table_widget_tasks.setCellWidget(row, 3, task.widget_profile)
			self.ui.table_widget_tasks.setCellWidget(row, 4, task.widget_product)
			self.ui.table_widget_tasks.setCellWidget(row, 5, task.widget_image)
			self.ui.table_widget_tasks.setCellWidget(row, 6, task.widget_proxy)
			self.ui.table_widget_tasks.setCellWidget(row, 7, task.widget_status)
			self.ui.table_widget_tasks.setCellWidget(row, 8, task.widget_action)
			self.ui.table_widget_tasks.resizeColumnToContents(8)

			self.tasks[task.task_id] = task

	def load_task_info(self, task_id):
		task = self.tasks[task_id]
		# self.ui.combo_box_task_type.setCurrentIndex(self.ui.combo_box_task_type.findText(str(task.task_type)))
		self.ui.combo_box_store.setCurrentIndex(self.ui.combo_box_store.findText(task.store_name))

		# Set after store is set
		self.ui.combo_box_task_type.setCurrentIndex(self.ui.combo_box_task_type.findText(task.task_type))
		# self.ui.combo_box_search_type.setCurrentIndex(self.ui.combo_box_search_type.findText(task.search_type))
		self.ui.line_edit_search.setText(task.search)
		self.ui.line_edit_task_name.setText(task.task_name)
		self.ui.line_edit_task_qty.setText('1')
		self.ui.combo_box_qty.setCurrentIndex(self.ui.combo_box_qty.findText(str(task.qty)))
		self.ui.check_box_account.setChecked(True if task.check_box_account else False)
		if task.account:
			self.ui.combo_box_accounts.setCurrentIndex(self.ui.combo_box_accounts.findData(task.account.account_id))
		self.ui.combo_box_profile.setCurrentIndex(self.ui.combo_box_profile.findData(task.profile.profile_id))
		self.ui.combo_box_billing.setCurrentIndex(self.ui.combo_box_billing.findData(task.billing.billing_id))
		self.ui.check_box_proxies.setChecked(True if task.check_box_proxies == 2 else False)
		if task.proxies:
			self.ui.combo_box_proxies.setCurrentIndex(self.ui.combo_box_proxies.findData(task.proxies.proxy_id))
		self.ui.combo_box_rotation.setCurrentIndex(self.ui.combo_box_rotation.findText(task.rotation))
		self.ui.check_box_size.setChecked(True if task.check_box_size == 2 else False)
		if self.ui.check_box_size.isChecked():
			self.ui.combo_box_size.setCurrentIndex(self.ui.combo_box_size.findText(task.size))
		self.ui.check_box_color.setChecked(True if task.check_box_color == 2 else False)
		if self.ui.check_box_color.isChecked():
			self.ui.line_edit_color.setText(task.color)
		self.ui.check_box_category.setChecked(True if task.check_box_category == 2 else False)
		if self.ui.check_box_category.isChecked():
			self.ui.combo_box_category.setCurrentIndex(self.ui.combo_box_category.findText(task.category))
		self.ui.check_box_price_range.setChecked(True if task.check_box_price_range == 2 else False)
		if self.ui.check_box_price_range.isChecked():
			self.ui.line_edit_price_min.setText(task.price_min)
			self.ui.line_edit_price_max.setText(task.price_max)
		self.ui.line_edit_delay_min.setText(task.delay_min)
		self.ui.line_edit_delay_max.setText(task.delay_max)
		self.ui.check_box_captcha.setChecked(True if task.check_box_captcha == 2 else False)

	def new_task(self):
		self.ui.combo_box_task_type.setCurrentIndex(-1)
		self.ui.combo_box_store.setCurrentIndex(-1)
		self.ui.combo_box_search_type.setCurrentIndex(-1)
		self.ui.line_edit_search.clear()
		self.ui.line_edit_task_name.clear()
		self.ui.line_edit_task_qty.setText(f'1')
		self.ui.combo_box_qty.setCurrentIndex(0)
		self.ui.combo_box_account.setCurrentIndex(-1)
		self.ui.combo_box_profile.setCurrentIndex(-1)
		self.ui.combo_box_billing.setCurrentIndex(-1)
		self.ui.check_box_proxies.setChecked(False)
		self.ui.combo_box_rotation.setCurrentIndex(0)
		self.ui.check_box_size.setChecked(False)
		self.ui.check_box_color.setChecked(False)
		self.ui.check_box_category.setChecked(False)
		self.ui.check_box_price_range.setChecked(False)
		self.ui.line_edit_delay_min.clear()
		self.ui.line_edit_delay_max.clear()
		self.ui.check_box_captcha.setChecked(False)
		# self.ui.table_widget_tasks.clearSelection()
		self.ui.table_widget_tasks.clearSelection()

	# def update_title(self, title):
	# 	self.ui.table_widget_tasks.setItem(row, 8, task.widget_status)
	# 	self.ui.label_product.setText(title)

	# def update_proxy(self, proxy, item):
	# 	row = self.ui.table_widget_tasks.row(item)
	# 	self.ui.table_widget_tasks.item(row, 7).setText(proxy)
	# 	self.ui.table_widget_tasks.resizeColumnToContents(7)

	def update_proxy(self, task_id):
		self.tasks[task_id].update_proxy()

	def update_product(self, product, item):
		row = self.ui.table_widget_tasks.row(item)
		self.ui.table_widget_tasks.item(row, 4).setText(product)
		self.ui.table_widget_tasks.resizeColumnToContents(4)

	def update_image(self, url, item):
		row = self.ui.table_widget_tasks.row(item)
		# self.ui.table_widget_tasks.item(row, 5)

		url_data = urllib.request.urlopen(url).read()
		image = QtGui.QImage()
		image.loadFromData(url_data)
		self.ui.label_picture.setPixmap(QtGui.QPixmap(image))

	def update_size(self, size, item):
		row = self.ui.table_widget_tasks.row(item)
		self.ui.table_widget_tasks.item(row, 6).setText(size)
		self.ui.table_widget_tasks.resizeColumnToContents(6)

	def request_abort(self, task_id):
		self.captcha_window.request_abort(task_id)

	def set_cookies(self, cookies, url):
		for cookie in cookies:
			self.browser.page().profile().cookieStore().setCookie(cookie)
		self.browser.loadFinished.connect(self.get_html)
		self.browser.load(QtCore.QUrl(url))

	def get_html(self):
		self.browser.page().toHtml(self.callable)

	def callable(self, data):
		print(data)

	def load_task_browser(self, task_id):
		self.tasks[task_id].render_browser()

		# self.view = QtWebEngineWidgets.QWebEngineView()
		# # self.cookie_store = self.view.page().profile().cookieStore()
		# for cookie in cookies:
		# 	print('name: {}'.format(cookie.name()))
		# 	print('value: {}'.format(cookie.value()))
		# 	print('domain: {}'.format(cookie.domain()))
		# 	self.view.page().profile().cookieStore().setCookie(cookie)
		# # self.view.page().profile().cookieStore().loadAllCookies()
		# self.view.loadFinished.connect(self.on_load_finished)
		# self.view.load(QtCore.QUrl(url))
		# self.view.show()

	def save_task(self):
		try:
			# Limit to numbers only and 2 digits using regex
			task_qty = int(self.ui.line_edit_task_qty.text())
			items = {
				'combo_box_task_type': self.ui.combo_box_task_type.currentText(),
				'combo_box_store': self.ui.combo_box_store.currentText(),
				'line_edit_custom_shopify': '',
				'combo_box_search_type': self.ui.combo_box_search_type.currentText(),
				'line_edit_search': self.ui.line_edit_search.text(),
				'line_edit_task_name': self.ui.line_edit_task_name.text(),
				'combo_box_qty': self.ui.combo_box_qty.currentText(),
				'check_box_account': self.ui.check_box_account.checkState(),
				'combo_box_account': self.ui.combo_box_account.currentData(QtCore.Qt.UserRole),
				'combo_box_profile': self.ui.combo_box_profile.currentData(QtCore.Qt.UserRole),
				'combo_box_billing': self.ui.combo_box_billing.currentData(QtCore.Qt.UserRole),
				'check_box_proxies': self.ui.check_box_proxies.checkState(),
				'combo_box_proxies': self.ui.combo_box_proxies.currentData(QtCore.Qt.UserRole),
				'combo_box_rotation': self.ui.combo_box_rotation.currentText(),
				'check_box_size': self.ui.check_box_size.checkState(),
				'combo_box_size': self.ui.combo_box_size.currentText(),
				'check_box_color': self.ui.check_box_color.checkState(),
				'line_edit_color': self.ui.line_edit_color.text(),
				'check_box_category': self.ui.check_box_category.checkState(),
				'combo_box_category': self.ui.combo_box_category.currentText(),
				'check_box_price_range': self.ui.check_box_price_range.checkState(),
				'line_edit_price_min': self.ui.line_edit_price_min.text(),
				'line_edit_price_max': self.ui.line_edit_price_max.text(),
				'line_edit_delay_min': self.ui.line_edit_delay_min.text(),
				'line_edit_delay_max': self.ui.line_edit_delay_max.text(),
				'check_box_captcha': self.ui.check_box_captcha.checkState()
			}
			task_name = items['line_edit_task_name']
			# Will only loop once for mass edit
			for i in range(0, task_qty):
				if self.task_ids:
					# Task(s) selected, update task(s)
					# for task_id in self.task_ids:

					# task_id = self.task_ids[0]
					# self.tgadb.save_task(items, task_id)
					pass
				else:
					# No task(s) selected, create new task
					self.tgadb.save_task(items)
					items['line_edit_task_name'] = f'{task_name} ({i + 1})'

				self.create_task(self.tgadb.get_recent_task())

			# Clear
			self.new_task()
		except Exception as e:
			print(f'{e}')
			self.confirmation_dialog('Error', 'Something went wrong.')

			



		# tasks = len(self.task_ids)
		# task_qty = int(self.ui.line_edit_task_qty.text())
		# if tasks < 1:
		# 	# Create new task
		# 	base_name = items['line_edit_task_name']
		# 	i = 0
		# 	while i < task_qty:
		# 		if i > 0:
		# 			items['line_edit_task_name'] = f'{base_name} ({i})'
		# 		self.tgadb.save_task(items)
		# 		data = self.tgadb.get_recent_task()
		# 		self.create_task(data)
		# 		i += 1
		# 	self.new_task()
		# elif tasks == 1:
		# 	# Update a task
		# 	base_name = items['line_edit_task_name']
		# 	i = 0
		# 	while i < task_qty:
		# 		if i > 0:
		# 			items['line_edit_task_name'] = f'{base_name} ({i})'
		# 			self.tgadb.save_task(items)
		# 			data = self.tgadb.get_recent_task()
		# 			self.create_task(data)
		# 		task_id = self.task_ids[0]
		# 		self.tgadb.save_task(items, task_id)
		# 		data = self.tgadb.get_task(task_id)
		# 		self.create_task(data, task_id=task_id, update=True)
		# 		i += 1
		# 	self.new_task()
		# else:
		# 	# Mass edit
		# 	fields = self.check_mass_edit_fields()
		# 	if fields:
		# 		for task_id in self.task_ids:
		# 			for key, value in fields.items():
		# 				self.tgadb.update_task(key, value, task_id)
		# 			data = self.tgadb.get_task(task_id)
		# 			self.create_task(data, task_id=task_id, update=True)
		# 		self.new_task()
		# 	else:
		# 		self.confirmation_dialog('Error', 'One or more fields are empty.')

	def delete_task(self, task_id, task_name):
		if self.confirmation_dialog('Confirm', 'Delete task [{}]?'.format(task_name)):
			self.tgadb.delete_task(task_id)
			row = self.ui.table_widget_tasks.row(self.tasks[task_id].widget_task_id)
			self.ui.table_widget_tasks.removeRow(row)
			del self.tasks[task_id]

	def error_on_delete_task(self, task_name):
		self.confirmation_dialog('Warning', 'Task [{}] is still running, please wait...'.format(task_name))

	def enable_mass_edit(self):
		for cb in self.cbe_items:
			cb.setChecked(False)
			# cb.setEnabled(True)
			cb.show()
		# for cb in self.mass_edit_items:
		# 	cb[0].setChecked(False)
		# 	cb[0].setEnabled(True)
		# 	cb[0].show()

		self.ui.label_tasks.setEnabled(False)
		self.ui.line_edit_task_qty.setEnabled(False)
		self.ui.line_edit_task_qty.clear()

		self.ui.combo_box_task_type.setCurrentIndex(-1)
		self.ui.combo_box_store.setCurrentIndex(-1)
		self.ui.combo_box_search_type.setCurrentIndex(-1)
		self.ui.line_edit_search.clear()
		self.ui.line_edit_task_name.clear()
		self.ui.combo_box_qty.setCurrentIndex(-1)
		self.ui.combo_box_account.setCurrentIndex(-1)
		self.ui.combo_box_profile.setCurrentIndex(-1)
		self.ui.combo_box_billing.setCurrentIndex(-1)
		self.ui.combo_box_proxies.setCurrentIndex(-1)
		self.ui.combo_box_rotation.setCurrentIndex(-1)
		self.ui.combo_box_size.setCurrentIndex(-1)
		self.ui.line_edit_color.clear()
		self.ui.combo_box_category.setCurrentIndex(-1)
		self.ui.line_edit_price_min.clear()
		self.ui.line_edit_price_max.clear()
		self.ui.line_edit_delay_min.clear()
		self.ui.line_edit_delay_max.clear()


	def disable_mass_edit(self):
		for cb in self.cbe_items:
			cb.setChecked(True)
			# cb.setEnabled(False)
			cb.hide()
		# for cb in self.mass_edit_items:
		# 	cb[0].setChecked(True)
		# 	cb[0].setEnabled(False)
		# 	cb[0].hide()

		self.ui.label_tasks.setEnabled(True)
		self.ui.line_edit_task_qty.setEnabled(True)
		self.ui.line_edit_task_qty.setText('1')

	def load_combo_box_profiles(self):
		self.ui.combo_box_profile.clear()
		for key, value in self.profiles.items():
			self.ui.combo_box_profile.addItem(value.profile_name, value.profile_id)

	def load_combo_box_billing(self):
		self.ui.combo_box_billing.clear()
		for key, value in self.billing.items():
			self.ui.combo_box_billing.addItem(value.billing_name, value.billing_id)

	def load_combo_box_proxies(self):
		self.ui.combo_box_proxies.clear()
		for key, value in self.proxies.items():
			self.ui.combo_box_proxies.addItem(value.proxy_name, value.proxy_id)

	def load_combo_box_categories(self):
		self.ui.combo_box_category.clear()
		self.ui.combo_box_category.addItem('New', 0)
		self.ui.combo_box_category.addItem('Accessories', 1)
		self.ui.combo_box_category.addItem('Bags', 2)
		self.ui.combo_box_category.addItem('Hats', 3)
		self.ui.combo_box_category.addItem('Jackets', 4)
		self.ui.combo_box_category.addItem('Pants', 5)
		self.ui.combo_box_category.addItem('Shirts', 6)
		self.ui.combo_box_category.addItem('Shoes', 7)
		self.ui.combo_box_category.addItem('Shorts', 8)
		self.ui.combo_box_category.addItem('Skate', 9)
		self.ui.combo_box_category.addItem('Sweatshirts', 10)
		self.ui.combo_box_category.addItem('T-Shirts', 11)
		self.ui.combo_box_category.addItem('Tops/Sweaters', 12)

	def load_combo_box_sizes(self):
		self.ui.combo_box_size.clear()
		self.ui.combo_box_size.addItem('Any', 0)
		self.ui.combo_box_size.addItem('Small', 1)
		self.ui.combo_box_size.addItem('Medium', 2)
		self.ui.combo_box_size.addItem('Medium +', 3)
		self.ui.combo_box_size.addItem('Large', 4)
		self.ui.combo_box_size.addItem('XLarge', 5)
		self.ui.combo_box_size.addItem('4', 6)
		self.ui.combo_box_size.addItem('4.5', 7)
		self.ui.combo_box_size.addItem('5', 8)
		self.ui.combo_box_size.addItem('5.5', 9)
		self.ui.combo_box_size.addItem('6', 10)
		self.ui.combo_box_size.addItem('6.5', 11)
		self.ui.combo_box_size.addItem('7', 12)
		self.ui.combo_box_size.addItem('7.5', 13)
		self.ui.combo_box_size.addItem('8', 14)
		self.ui.combo_box_size.addItem('8.5', 15)
		self.ui.combo_box_size.addItem('9', 16)
		self.ui.combo_box_size.addItem('9.5', 17)
		self.ui.combo_box_size.addItem('10', 18)
		self.ui.combo_box_size.addItem('10.5', 19)
		self.ui.combo_box_size.addItem('11', 20)
		self.ui.combo_box_size.addItem('11.5', 21)
		self.ui.combo_box_size.addItem('12', 22)
		self.ui.combo_box_size.addItem('12.5', 23)
		self.ui.combo_box_size.addItem('13', 24)
		self.ui.combo_box_size.addItem('13.5', 25)
		self.ui.combo_box_size.addItem('14', 26)

#================================================================================
# PROFILE PAGE
#================================================================================

	def load_profile_list(self):
		self.create_profile(self.tgadb.get_all_profiles())

	def load_profile_info(self, profile_id):
		profile = self.profiles[profile_id]
		self.ui.line_edit_profile_name.setText(profile.profile_name)
		self.ui.check_box_email_jig.setCheckState(profile.check_box_email_jig)
		self.ui.line_edit_email.setText(profile.email)
		self.ui.line_edit_phone.setText(profile.phone)
		self.ui.line_edit_s_first_name.setText(profile.s_first_name)
		self.ui.line_edit_s_last_name.setText(profile.s_last_name)
		self.ui.line_edit_s_address_1.setText(profile.s_address_1)
		self.ui.line_edit_s_address_2.setText(profile.s_address_2)
		self.ui.line_edit_s_city.setText(profile.s_city)
		self.ui.combo_box_s_state.setCurrentIndex(self.ui.combo_box_s_state.findText(profile.s_state))
		self.ui.line_edit_s_zip.setText(profile.s_zip)
		self.ui.gb_billing.setChecked(True if profile.group_box_same_as_shipping == 2 else False)
		# self.ui.gb_billing.setCheckState(profile.group_box_same_as_shipping)
		self.ui.line_edit_b_first_name.setText(profile.b_first_name)
		self.ui.line_edit_b_last_name.setText(profile.b_last_name)
		self.ui.line_edit_b_address_1.setText(profile.b_address_1)
		self.ui.line_edit_b_address_2.setText(profile.b_address_2)
		self.ui.line_edit_b_city.setText(profile.b_city)
		self.ui.combo_box_b_state.setCurrentIndex(self.ui.combo_box_b_state.findText(profile.b_state))
		self.ui.line_edit_b_zip.setText(profile.b_zip)

	def new_profile(self):
		self.ui.line_edit_profile_name.clear()
		self.ui.check_box_email_jig.setCheckState(QtCore.Qt.Checked)
		self.ui.line_edit_email.clear()
		self.ui.line_edit_phone.clear()
		self.ui.line_edit_s_first_name.clear()
		self.ui.line_edit_s_last_name.clear()
		self.ui.line_edit_s_address_1.clear()
		self.ui.line_edit_s_address_2.clear()
		self.ui.line_edit_s_city.clear()
		self.ui.combo_box_s_state.setCurrentIndex(0)
		self.ui.line_edit_s_zip.clear()
		self.ui.gb_billing.setChecked(True)
		self.ui.line_edit_b_first_name.clear()
		self.ui.line_edit_b_last_name.clear()
		self.ui.line_edit_b_address_1.clear()
		self.ui.line_edit_b_address_2.clear()
		self.ui.line_edit_b_city.clear()
		self.ui.combo_box_b_state.setCurrentIndex(0)
		self.ui.line_edit_b_zip.clear()
		self.ui.list_widget_profiles.clearSelection()

	def create_profile(self, profile_data):
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t in profile_data:
			profile = Profile(
				profile_id=a,
				profile_name=b,
				check_box_email_jig=c,
				email=d,
				phone=e,
				s_first_name=f,
				s_last_name=g,
				s_address_1=h,
				s_address_2=i,
				s_city=j,
				s_state=k,
				s_zip=l,
				group_box_same_as_shipping=m,
				b_first_name=n,
				b_last_name=o,
				b_address_1=p,
				b_address_2=q,
				b_city=r,
				b_state=s,
				b_zip=t
			)
			item = QtWidgets.QListWidgetItem(profile.profile_name)
			item.setData(QtCore.Qt.UserRole, profile.profile_id)
			self.ui.list_widget_profiles.addItem(item)
			self.ui.combo_box_profile.addItem(profile.profile_name, profile.profile_id)
			self.profiles[profile.profile_id] = profile

	def save_profile(self):
		item = self.ui.list_widget_profiles.currentItem()
		items = {
			'profile_name': self.ui.line_edit_profile_name.text(),
			'check_box_email_jig': self.ui.check_box_email_jig.checkState(),
			'email': self.ui.line_edit_email.text(),
			'phone': self.ui.line_edit_phone.text(),
			's_first_name': self.ui.line_edit_s_first_name.text(),
			's_last_name': self.ui.line_edit_s_last_name.text(),
			's_address_1': self.ui.line_edit_s_address_1.text(),
			's_address_2': self.ui.line_edit_s_address_2.text(),
			's_city': self.ui.line_edit_s_city.text(),
			's_state': self.ui.combo_box_s_state.currentText(),
			's_zip': self.ui.line_edit_s_zip.text(),
			'group_box_same_as_shipping': 2 if self.ui.gb_billing.isChecked() else 0,
			'b_first_name': self.ui.line_edit_b_first_name.text(),
			'b_last_name': self.ui.line_edit_b_last_name.text(),
			'b_address_1': self.ui.line_edit_b_address_1.text(),
			'b_address_2': self.ui.line_edit_b_address_2.text(),
			'b_city': self.ui.line_edit_b_city.text(),
			'b_state': self.ui.combo_box_b_state.currentText(),
			'b_zip': self.ui.line_edit_b_zip.text()
		}
		self.tgadb.save_profile(items)
		self.create_profile(self.tgadb.get_recent_profile())
		self.new_profile()

	def delete_profile(self, profile_item):
		# Grab ID and ROW from billing item
		if self.confirmation_dialog('Please Confirm', f'Are you sure you want to delete [{profile_item.text()}]'):
			# delete from database
			try:
				profile_id = profile_item.data(QtCore.Qt.UserRole)
				row = self.ui.list_widget_profiles.row(profile_item)
				self.ui.list_widget_profiles.takeItem(row)
				self.tgadb.delete_profile(profile_id)
				self.new_profile()
				self.profiles.pop(profile_id)
				self.ui.combo_box_profile.removeItem(self.ui.combo_box_profile.findData(profile_id))
			except Exception as e:
				print(f'{e}')

		# self.load_combo_box_profiles()

	def delete_all_profiles(self):
		# prompt dialog for "are you sure" before deleting
		if self.confirmation_dialog('Please Confirm', 'Are you sure you want to delete all profiles?'):
			try:
				self.tgadb.delete_all_profiles()
			except Exception as e:
				self.post_to_log('Error deleting all profiles [{}]'.format(str(e)))
			else:
				# clear fields
				self.new_profile()
				# post to log
				self.post_to_log('Deleted all profiles successfully')
				# clear list widget profiles
				self.ui.list_widget_profiles.clear()
				# clear selections
				self.ui.list_widget_profiles.clearSelection()
				self.ui.list_widget_profiles.selectionModel().clear()
				# update combo box billing profile
				self.load_combo_box_billing()

	def same_as_shipping(self):
		if self.ui.check_box_same_as_shipping.isChecked():
			for pair in self.profile_pairs:
				if type(pair[0]) is QtWidgets.QLineEdit:
					pair[0].setText(pair[1].text())
				elif type(pair[0]) is QtWidgets.QComboBox:
					pair[0].setCurrentIndex(pair[1].currentIndex())
				pair[0].setEnabled(False)
		else:
			for pair in self.profile_pairs:
				if type(pair[0]) is QtWidgets.QLineEdit:
					pair[0].clear()
				elif type(pair[0]) is QtWidgets.QComboBox:
					pair[0].setCurrentIndex(0)
				pair[0].setEnabled(True)

#================================================================================
# BILLING PAGE
#================================================================================

	def load_billing_list(self):
		self.create_billing_profile(self.tgadb.get_all_billing())

	def load_billing_info(self, billing_id):
		billing = self.billing[billing_id]
		self.ui.line_edit_billing_name.setText(billing.billing_name)
		self.ui.line_edit_card_name.setText(billing.card_name)
		self.ui.line_edit_card_number.setText(billing.card_number)
		self.ui.combo_box_card_month.setCurrentIndex(self.ui.combo_box_card_month.findText(billing.card_month))
		self.ui.combo_box_card_year.setCurrentIndex(self.ui.combo_box_card_year.findText(billing.card_year))
		self.ui.line_edit_card_cvv.setText(billing.card_cvv)

	def new_billing_profile(self):
		self.ui.line_edit_billing_name.clear()
		self.ui.line_edit_card_name.clear()
		self.ui.line_edit_card_number.clear()
		self.ui.combo_box_card_month.setCurrentIndex(0)
		self.ui.combo_box_card_year.setCurrentIndex(0)
		self.ui.line_edit_card_cvv.clear()
		
		self.ui.list_widget_billing.clearSelection()
		# self.ui.list_widget_billing.selectionModel().clear()

	def create_billing_profile(self, billing_data):
		for a, b, c, d, e, f, g in billing_data:
			billing = Billing(
				billing_id=a,
				billing_name=b,
				card_name=c,
				card_number=d,
				card_month=e,
				card_year=f,
				card_cvv=g
			)
			item = QtWidgets.QListWidgetItem(billing.billing_name)
			item.setData(QtCore.Qt.UserRole, billing.billing_id)
			self.ui.list_widget_billing.addItem(item)
			self.ui.combo_box_billing.addItem(billing.billing_name, billing.billing_id)
			self.billing[billing.billing_id] = billing

	def save_billing_profile(self):
		# item = self.ui.list_widget_billing.currentItem()
		items = {
			'billing_name': self.ui.line_edit_billing_name.text(),
			'card_name': self.ui.line_edit_card_name.text(),
			'card_number': self.ui.line_edit_card_number.text(),
			'card_month': self.ui.combo_box_card_month.currentText(),
			'card_year': self.ui.combo_box_card_year.currentText(),
			'card_cvv': self.ui.line_edit_card_cvv.text()
		}
		self.tgadb.save_billing(items)
		self.create_billing_profile(self.tgadb.get_recent_billing())
		self.new_billing_profile()
		# 	self.post_to_log('One or more fields are empty')

	def delete_billing_profile(self, billing_item):
		# Grab ID and ROW from billing item
		if self.confirmation_dialog('Please Confirm', f'Are you sure you want to delete [{billing_item.text()}]'):
			# delete from database
			try:
				billing_id = billing_item.data(QtCore.Qt.UserRole)
				row = self.ui.list_widget_billing.row(billing_item)
				self.ui.list_widget_billing.takeItem(row)
				self.tgadb.delete_billing(billing_id)
				self.new_billing_profile()
				self.billing.pop(billing_id)
				self.ui.combo_box_billing.removeItem(self.ui.combo_box_billing.findData(billing_id))
			except Exception as e:
				print(f'{e}')

	def delete_all_billing_profiles(self):
		# prompt dialog for "are you sure" before deleting
		if self.confirmation_dialog('Pleas Confirm', 'Are you sure you want to delete all billing?'):
			try:
				self.tgadb.delete_all_billing()
			except Exception as e:
				self.post_to_log('Error deleting all billing profiles [{}]'.format(str(e)))
			else:
				# post to log
				self.post_to_log('Deleted all billing profiles successfully')
				# clear fields
				self.new_billing_profile()
				self.ui.list_widget_billing.clear()
				# clear selections
				self.ui.list_widget_billing.clearSelection()
				self.ui.list_widget_billing.selectionModel().clear()
				# update combo box billing profile
				self.load_combo_box_billing()

#================================================================================
# PROXY PAGE
#================================================================================

	def load_proxy_list(self):
		self.create_proxy_profile(self.tgadb.get_all_proxies())

	def load_proxy_info(self, proxy_id):
		proxy = self.proxies[proxy_id]
		self.ui.line_edit_proxy_name.setText(proxy.proxy_name)
		self.ui.plain_text_edit_proxies.setPlainText(proxy.proxies)
		# data = self.tgadb.get_proxy(proxy_id)
		# if data:
		# 	for a, b, c in data:
		# 		self.proxy = Proxy(a, b, c)
		# 		# proxy_id = a
		# 		# proxy_name = b
		# 		# proxies = c
		# 	self.ui.line_edit_proxy_name.setText(self.proxy.proxy_name)
		# 	self.ui.plain_text_edit_proxies.setPlainText(self.proxy.proxies)

		# 	# clear rows before inserting
		# 	# self.ui.table_widget_proxies.setRowCount(0)
		# 	# row = 0
		# 	# for item in self.proxy.proxies.split('\n'):
		# 	# 	self.ui.table_widget_proxies.insertRow(self.ui.table_widget_proxies.rowCount())
		# 	# 	self.ui.table_widget_proxies.setItem(row, 0, QtWidgets.QTableWidgetItem(item))
		# 	# 	self.ui.table_widget_proxies.setCellWidget(row, 2, self.proxy.button_widgets[row])
		# 	# 	# print(proxy.buttons[row])
		# 	# 	row += 1
		# else:
		# 	print('there is no data')

	def new_proxy_profile(self):
		self.ui.line_edit_proxy_name.clear()
		self.ui.plain_text_edit_proxies.clear()
		self.ui.list_widget_proxies.clearSelection()

	def create_proxy_profile(self, proxy_data):
		for a, b, c in proxy_data:
			proxy = Proxy(
				proxy_id=a,
				proxy_name=b,
				proxies=c
			)
			item = QtWidgets.QListWidgetItem(proxy.proxy_name)
			item.setData(QtCore.Qt.UserRole, proxy.proxy_id)
			self.ui.list_widget_proxies.addItem(item)
			self.ui.combo_box_proxies.addItem(proxy.proxy_name, proxy.proxy_id)
			self.proxies[proxy.proxy_id] = proxy

	def save_proxy_profile(self):
		# item = self.ui.list_widget_proxies.currentItem()
		items = {
			'proxy_name': self.ui.line_edit_proxy_name.text(),
			'proxies': self.ui.plain_text_edit_proxies.toPlainText()
		}
		self.tgadb.save_proxy(items)
		self.create_proxy_profile(self.tgadb.get_recent_proxy())
		self.new_proxy_profile()
		# validate items
		# if self.validate_fields(self.proxy_items):
		# 	try:
		# 		if item:
		# 			self.tgadb.save_proxy(items, item.data(QtCore.Qt.UserRole))
		# 		else:
		# 			self.tgadb.save_proxy(items)
		# 	except Exception as e:
		# 		self.post_to_log('Error saving proxy profile [{}]'.format(str(e)))
		# 	else:
		# 		if item:
		# 			self.post_to_log('Proxy profile [{}] updated successfully'.format(items['proxy_name']))
		# 		else:
		# 			self.post_to_log('Proxy profile [{}] saved successfully'.format(items['proxy_name'])) # post to console/log
		# 		# clear fields
		# 		self.new_proxy_profile()
		# 		# update list widget proxies (addItem)
		# 		self.ui.list_widget_proxies.clear()
		# 		self.ui.list_widget_proxies.clearSelection()
		# 		self.ui.list_widget_proxies.selectionModel().clear()
		# 		self.load_proxy_list()
		# 		# update combo box proxies profile
		# 		self.load_combo_box_proxies()
		# else:
		# 	self.post_to_log('One or more fields are empty')

	def delete_proxy_profile(self, proxy_item):
		# Grab ID and ROW from proxy item
		if self.confirmation_dialog('Please Confirm', f'Are you sure you want to delete [{proxy_item.text()}]'):
			# delete from database
			try:
				proxy_id = proxy_item.data(QtCore.Qt.UserRole)
				row = self.ui.list_widget_proxies.row(proxy_item)
				self.ui.list_widget_proxies.takeItem(row)
				self.tgadb.delete_proxy(proxy_id)
				self.new_proxy_profile()
				self.proxies.pop(proxy_id)
				self.ui.combo_box_proxies.removeItem(self.ui.combo_box_proxies.findData(proxy_id))
			except Exception as e:
				print(f'{e}')

	def delete_all_proxy_profiles(self):
		# prompt dialog for "are you sure" before deleting
		if self.confirmation_dialog('Please Confirm', 'Are you sure you want to delete all proxy profiles?'):
			try:
				self.ui.combo_box_proxies.clear()
				self.ui.list_widget_proxies.clear()
				self.tgadb.delete_all_proxies()
				self.proxies = {}
			except Exception as e:
				print(f'{e}')

	def import_proxies(self):
		# print(type(self.open_file()))
		self.ui.plain_text_edit_proxies.setPlainText(self.open_file())

	def update_proxy_count(self):
		i = self.ui.plain_text_edit_proxies.toPlainText().splitlines()
		self.ui.label_proxy_count.setText(f'{len(i)}')

	def open_file(self):
		file_path = QtWidgets.QFileDialog.getOpenFileName(filter='*.txt')
		if file_path[0]:
			with open('{}'.format(file_path[0])) as file:
				return file.read()

# Initialize global database
def init_db():
	tgadb = TheGeckoAppDatabase('gecko.db')
	tgadb.create_table_keys()
	tgadb.create_table_tasks()
	tgadb.create_table_profiles()
	tgadb.create_table_billing()
	tgadb.create_table_proxies()
	tgadb.create_table_accounts()
	return tgadb

# scale for hi resolution displays
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

if __name__ == "__main__":
	sys.argv.append("--disable-web-security")
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseOpenGLES, True)
	app = QtWidgets.QApplication(sys.argv)
	tgadb = init_db()
	# activation_window = ActivationGUI(tgadb)
	# activation_window.show()
	# if activation_window.exec_():
	# 	MainWindow = GUI(tgadb)
	# 	MainWindow.show()
	# 	MainWindow.export_main_log()
	# 	exit = app.exec_()
	# 	sys.exit(exit)

	MainWindow = GUI(tgadb)
	MainWindow.show()
	MainWindow.export_main_log()
	exit = app.exec_()
	sys.exit(exit)

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())