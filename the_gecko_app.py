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

VERSION = 'The Gecko App v0.0.8'

class GUI(QtWidgets.QMainWindow):

	def __init__(self, db):
		super().__init__()
		# app = QtWidgets.QApplication(sys.argv)
		# MainWindow = QtWidgets.QMainWindow()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Tab Task paired controls
		self.row_task_type = [self.ui.cbe_task_type, self.ui.label_task_type, self.ui.combo_box_task_type, self.ui.label_tasks, self.ui.line_edit_task_qty]
		self.row_task_name = [self.ui.cbe_task_name, self.ui.label_task_name, self.ui.line_edit_task_name]
		self.row_store = [self.ui.cbe_store, self.ui.label_store, self.ui.combo_box_store, self.ui.line_edit_custom_shopify, self.ui.push_button_test_custom_shopify, self.ui.label_tested]
		self.row_search_type = [self.ui.cbe_search_type, self.ui.label_search_type, self.ui.combo_box_search_type]
		self.row_account = [self.ui.cbe_account, self.ui.check_box_account, self.ui.combo_box_accounts]
		self.row_profile = [self.ui.cbe_profile, self.ui.label_profile, self.ui.combo_box_profiles]
		self.row_billing = [self.ui.cbe_billing, self.ui.label_billing, self.ui.combo_box_billing]
		self.row_proxies = [self.ui.cbe_proxies, self.ui.check_box_proxies, self.ui.combo_box_proxies]
		self.row_rotation = [self.ui.cbe_rotation, self.ui.label_rotation, self.ui.combo_box_rotation]
		self.row_search = [self.ui.cbe_search, self.ui.label_search, self.ui.line_edit_search]
		self.row_category = [self.ui.cbe_category, self.ui.check_box_category, self.ui.combo_box_category]
		self.row_size = [self.ui.cbe_size, self.ui.check_box_size, self.ui.combo_box_size]
		self.row_color = [self.ui.cbe_color, self.ui.check_box_color, self.ui.line_edit_color]
		self.row_retry = [self.ui.cbe_retry_delay, self.ui.label_retry_delay, self.ui.line_edit_retry_delay, self.ui.label_retry_ms, self.ui.label_retry_range]
		self.row_retry_variance = [self.ui.cbe_retry_variance, self.ui.check_box_retry_variance, self.ui.line_edit_retry_variance, self.ui.label_retry_var_ms]
		self.row_checkout = [self.ui.cbe_checkout_delay, self.ui.check_box_checkout_delay, self.ui.line_edit_checkout_delay, self.ui.label_checkout_ms, self.ui.label_checkout_range]
		self.row_checkout_variance = [self.ui.cbe_checkout_variance, self.ui.check_box_checkout_variance, self.ui.line_edit_checkout_variance, self.ui.label_checkout_var_ms]
		self.row_qty = [self.ui.cbe_qty, self.ui.label_qty, self.ui.combo_box_qty]
		self.row_captcha = [self.ui.cbe_captcha, self.ui.check_box_captcha]

		self.cbe_items = [
			self.ui.cbe_task_type,
			self.ui.cbe_store,
			self.ui.cbe_search_type,
			self.ui.cbe_search,
			self.ui.cbe_task_name,
			self.ui.cbe_account,
			self.ui.cbe_profile,
			self.ui.cbe_billing,
			self.ui.cbe_proxies,
			self.ui.cbe_rotation,
			self.ui.cbe_category,
			self.ui.cbe_size,
			self.ui.cbe_color,
			self.ui.cbe_retry_delay,
			self.ui.cbe_retry_variance,
			self.ui.cbe_checkout_delay,
			self.ui.cbe_checkout_variance,
			self.ui.cbe_qty,
			self.ui.cbe_captcha
		]

		self.num_only_line_edits = [
			self.ui.line_edit_retry_delay,
			self.ui.line_edit_retry_variance,
			self.ui.line_edit_checkout_delay,
			self.ui.line_edit_checkout_variance,
			self.ui.line_edit_task_qty,
			self.ui.line_edit_phone,
			self.ui.line_edit_card_number,
			self.ui.line_edit_cvv
		]

		self.profile_pairs = [
			[self.ui.line_edit_billing_address, self.ui.line_edit_shipping_address],
			[self.ui.line_edit_billing_address_2, self.ui.line_edit_shipping_address_2],
			[self.ui.line_edit_billing_city, self.ui.line_edit_shipping_city],
			[self.ui.combo_box_billing_state, self.ui.combo_box_shipping_state],
			[self.ui.line_edit_billing_zip, self.ui.line_edit_shipping_zip]
		]

		# Check if LineEdit, QComboBox is not empty enum
		self.task_fields = [
			self.ui.combo_box_task_type,
			self.ui.combo_box_store,
			self.ui.combo_box_search_type,
			self.ui.line_edit_search,
			self.ui.line_edit_task_name,
			self.ui.line_edit_task_qty,
			self.ui.combo_box_profiles,
			self.ui.combo_box_billing,
			self.ui.combo_box_proxies,
			self.ui.combo_box_rotation,
			self.ui.line_edit_search,
			self.ui.combo_box_category,
			self.ui.combo_box_size,
			self.ui.line_edit_color,
			self.ui.line_edit_retry_delay,
			self.ui.line_edit_retry_variance,
			self.ui.line_edit_checkout_delay,
			self.ui.line_edit_checkout_variance,
			self.ui.combo_box_qty
		]

		self.task_fields_any = [
			self.ui.line_edit_task_name,
			self.ui.combo_box_profiles,
			self.ui.combo_box_billing,
			self.ui.combo_box_proxies,
			# self.ui.line_edit_direct_link,
			self.ui.line_edit_search,
			# self.ui.line_edit_neg_kw,
			self.ui.combo_box_category,
			self.ui.combo_box_size,
			self.ui.line_edit_color,
		]

		self.task_fields_num = [
			self.ui.line_edit_task_qty,
			self.ui.line_edit_retry_delay,
			self.ui.line_edit_retry_variance,
			self.ui.line_edit_checkout_delay,
			self.ui.line_edit_checkout_variance
		]

		self.profile_items = [
			self.ui.line_edit_profile_name,
			self.ui.line_edit_first_name,
			self.ui.line_edit_last_name,
			self.ui.line_edit_email,
			self.ui.line_edit_phone,
			self.ui.line_edit_shipping_address,
			self.ui.line_edit_shipping_city,
			self.ui.combo_box_shipping_state,
			self.ui.line_edit_shipping_zip,
			self.ui.line_edit_billing_address,
			self.ui.line_edit_billing_city,
			self.ui.combo_box_billing_state,
			self.ui.line_edit_billing_zip
		]

		self.address_pair = [self.ui.line_edit_shipping_address, self.ui.line_edit_billing_address]
		self.address_2_pair = [self.ui.line_edit_shipping_address_2, self.ui.line_edit_billing_address_2]
		self.city_pair = [self.ui.line_edit_shipping_city, self.ui.line_edit_billing_city]
		self.zip_pair = [self.ui.line_edit_shipping_zip, self.ui.line_edit_billing_zip]
		self.state_pair = [self.ui.combo_box_shipping_state, self.ui.combo_box_billing_state]

		self.billing_items = [
			self.ui.line_edit_billing_name,
			self.ui.line_edit_name_on_card,
			self.ui.combo_box_card_type,
			self.ui.line_edit_card_number,
			self.ui.combo_box_exp_month,
			self.ui.combo_box_exp_year,
			self.ui.line_edit_cvv
		]

		self.proxy_items = [
			self.ui.line_edit_proxy_name,
			self.ui.plain_text_edit_proxies
		]

		self.task_edit_items = [
			[self.ui.cbe_task_type, self.ui.combo_box_task_type],
			[self.ui.cbe_task_name, self.ui.line_edit_task_name],
			[self.ui.cbe_store, self.ui.combo_box_store],
			[self.ui.cbe_search_type, self.ui.combo_box_search_type],
			[self.ui.cbe_profile, self.ui.combo_box_profiles],
			[self.ui.cbe_proxies, self.ui.check_box_proxies, self.ui.combo_box_proxies],
			[self.ui.cbe_search, self.ui.line_edit_search],
			[self.ui.cbe_category, self.ui.check_box_category, self.ui.combo_box_category],
			[self.ui.cbe_size, self.ui.check_box_size, self.ui.combo_box_size],
			[self.ui.cbe_color, self.ui.check_box_color, self.ui.line_edit_color],
			[self.ui.cbe_retry_delay, self.ui.line_edit_retry_delay, self.ui.check_box_retry_variance, self.ui.line_edit_retry_variance],
			[self.ui.cbe_checkout_delay, self.ui.check_box_checkout_delay, self.ui.line_edit_checkout_delay, self.ui.check_box_checkout_variance, self.ui.line_edit_checkout_variance],
			[self.ui.cbe_qty, self.ui.combo_box_qty]
		]

		self.stores = [
			'Custom Shopify',
			'https://www.bestbuy.ca/',
			'https://www.bestbuy.com/',
			'https://www.hottopic.com/',
			'https://www.hyperxgaming.com/',
			'https://www.shopdisney.com/',
			'https://www.supremenewyork.com/',
			'https://www.target.com/'
		]

		self.ui.combo_box_store.addItem(self.stores[0], 'nk')
		self.ui.combo_box_store.addItem(self.stores[1], 'nv')
		self.ui.combo_box_store.addItem(self.stores[2], 'nv')
		self.ui.combo_box_store.addItem(self.stores[3], 'nk')
		self.ui.combo_box_store.addItem(self.stores[4], 'nv')
		self.ui.combo_box_store.addItem(self.stores[5], 'nv')
		self.ui.combo_box_store.addItem(self.stores[6], 'nk')
		self.ui.combo_box_store.addItem(self.stores[7], 'nv')

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
		self.icon_logo = QtGui.QPixmap(QtGui.QImage('src/logo_2.png').scaled(232, 232, QtCore.Qt.KeepAspectRatio))
		self.ui.label_picture.setPixmap(self.icon_logo)
		self.proxy = None
		self.proxies = {}
		self.tasks = {}
		self.task_ids = []
		self.accounts = {}
		self.tokens = {}
		self.token_count = 0
		self.solvers = {}
		self.mass_edit_fields = {}
		# self.highlight_rows = {}
		self.renderers = {}
		self.ctrl_key = False
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

		# create captcha queue types
		self.tokens = {}
		for store in self.stores:
			self.tokens[store] = queue.Queue()

		# rx = QtCore.QRegExp('^[0-9]{1,}$')
		rx = QtCore.QRegExp('^([1-9][0-9]*)$')
		self.validator = QtGui.QRegExpValidator(rx, self)
		for item in self.num_only_line_edits:
			item.setValidator(self.validator)

		# --------------------Recaptcha Window--------------------

		# --------------------Icons--------------------
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

		self.row_task_type[0].stateChanged.connect(self.toggle_row_task_type)
		self.row_task_name[0].stateChanged.connect(self.toggle_row_task_name)
		self.row_store[0].stateChanged.connect(self.toggle_row_store)
		self.row_store[2].currentIndexChanged.connect(self.toggle_custom_shopify)
		self.row_search_type[0].stateChanged.connect(self.toggle_row_search_type)
		self.row_account[0].stateChanged.connect(self.toggle_row_account)
		self.row_account[1].stateChanged.connect(self.toggle_accounts)
		self.row_profile[0].stateChanged.connect(self.toggle_row_profile)
		self.row_billing[0].stateChanged.connect(self.toggle_row_billing)
		self.row_proxies[0].stateChanged.connect(self.toggle_row_proxies)
		self.row_proxies[1].stateChanged.connect(self.toggle_proxies)
		self.row_rotation[0].stateChanged.connect(self.toggle_row_rotation)
		self.row_search[0].stateChanged.connect(self.toggle_row_search)
		self.row_category[0].stateChanged.connect(self.toggle_row_category)
		self.row_category[1].stateChanged.connect(self.toggle_category)
		self.row_size[0].stateChanged.connect(self.toggle_row_size)
		self.row_size[1].stateChanged.connect(self.toggle_size)
		self.row_color[0].stateChanged.connect(self.toggle_row_color)
		self.row_color[1].stateChanged.connect(self.toggle_color)
		self.row_retry[0].stateChanged.connect(self.toggle_row_retry)
		self.row_retry_variance[0].stateChanged.connect(self.toggle_row_retry_variance)
		self.row_retry_variance[1].stateChanged.connect(self.toggle_retry_variance)
		self.row_checkout[0].stateChanged.connect(self.toggle_row_checkout)
		self.row_checkout[1].stateChanged.connect(self.toggle_checkout)
		self.row_checkout_variance[0].stateChanged.connect(self.toggle_row_checkout_variance)
		self.row_checkout_variance[1].stateChanged.connect(self.toggle_checkout_variance)
		self.row_qty[0].stateChanged.connect(self.toggle_row_qty)
		self.row_captcha[0].stateChanged.connect(self.toggle_row_captcha)
		# self.row_captcha[1].stateChanged.connect(self.toggle_captcha)
		# self.ui.table_widget_tasks.cellEntered.connect(self.test6)

		# --------------------Task Buttons--------------------
		self.ui.push_button_new_task.clicked.connect(self.new_task)
		self.ui.push_button_save_task.clicked.connect(self.save_task)

		self.ui.label_picture.setScaledContents(False)
		self.ui.combo_box_store.currentIndexChanged.connect(self.load_types)
		self.ui.push_button_start_tasks.setText('Start All')
		self.ui.push_button_start_tasks.clicked.connect(self.start_tasks)
		self.ui.push_button_stop_tasks.setText('Stop All')
		self.ui.push_button_stop_tasks.clicked.connect(self.stop_tasks)
		self.ui.push_button_delete_tasks.setText('Delete All')
		self.ui.push_button_delete_tasks.clicked.connect(self.delete_all_tasks)
		self.ui.line_edit_retry_delay.textChanged.connect(lambda: self.update_delay_label(self.ui.label_retry, self.ui.line_edit_retry_delay, self.ui.line_edit_retry_variance))
		self.ui.line_edit_retry_variance.textChanged.connect(lambda: self.update_delay_label(self.ui.label_retry, self.ui.line_edit_retry_delay, self.ui.line_edit_retry_variance))
		self.ui.line_edit_checkout_delay.textChanged.connect(lambda: self.update_delay_label(self.ui.label_checkout, self.ui.line_edit_checkout_delay, self.ui.line_edit_checkout_variance))
		self.ui.line_edit_checkout_variance.textChanged.connect(lambda: self.update_delay_label(self.ui.label_checkout, self.ui.line_edit_checkout_delay, self.ui.line_edit_checkout_variance))
		self.ui.push_button_test_custom_shopify.clicked.connect(self.test_shopify)

		# --------------------Profile Buttons--------------------
		self.ui.push_button_new_profile.clicked.connect(self.new_profile)
		self.ui.push_button_save_profile.clicked.connect(self.save_profile)
		self.ui.push_button_delete_all_profiles.clicked.connect(self.delete_all_profiles)
		self.ui.push_button_delete_profile.clicked.connect(lambda: self.delete_profile(self.ui.list_widget_profiles.currentItem().data(QtCore.Qt.UserRole)))
		self.ui.list_widget_profiles.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_profiles, self.ui.push_button_delete_profile))
		self.ui.list_widget_profiles.clicked.connect(lambda: self.load_profile_info(self.ui.list_widget_profiles.currentItem().data(QtCore.Qt.UserRole)))
		self.ui.check_box_same_as_shipping.toggled.connect(self.same_as_shipping)
		self.ui.line_edit_shipping_address.textChanged.connect(lambda: self.copy_text(self.address_pair))
		self.ui.line_edit_shipping_address_2.textChanged.connect(lambda: self.copy_text(self.address_2_pair))
		self.ui.line_edit_shipping_city.textChanged.connect(lambda: self.copy_text(self.city_pair))
		self.ui.line_edit_shipping_zip.textChanged.connect(lambda: self.copy_text(self.zip_pair))
		self.ui.combo_box_shipping_state.currentIndexChanged.connect(lambda: self.copy_index(self.state_pair))

		# --------------------Billing Buttons--------------------
		self.ui.push_button_new_billing.clicked.connect(self.new_billing_profile)
		self.ui.push_button_save_billing.clicked.connect(self.save_billing_profile)
		self.ui.push_button_delete_all_billing.clicked.connect(self.delete_all_billing_profiles)
		self.ui.push_button_delete_billing.clicked.connect(lambda: self.delete_billing_profile(self.ui.list_widget_billing.currentItem().data(QtCore.Qt.UserRole)))
		self.ui.list_widget_billing.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_billing, self.ui.push_button_delete_billing))
		self.ui.list_widget_billing.clicked.connect(lambda: self.load_billing_info(self.ui.list_widget_billing.currentItem().data(QtCore.Qt.UserRole)))

		# --------------------Proxy Buttons--------------------
		self.ui.push_button_new_proxies.clicked.connect(self.new_proxy_profile)
		self.ui.push_button_import_proxies.clicked.connect(self.import_proxies)
		self.ui.push_button_save_proxies.clicked.connect(self.save_proxy_profile)
		self.ui.push_button_delete_all_proxies.clicked.connect(self.delete_all_proxy_profiles)
		self.ui.push_button_delete_proxies.clicked.connect(lambda: self.delete_proxy_profile(self.ui.list_widget_proxies.currentItem().data(QtCore.Qt.UserRole)))
		self.ui.list_widget_proxies.itemSelectionChanged.connect(lambda: self.toggle_button(self.ui.list_widget_proxies, self.ui.push_button_delete_proxies))
		self.ui.plain_text_edit_proxies.textChanged.connect(self.update_proxy_count)
		self.ui.list_widget_proxies.clicked.connect(lambda: self.load_proxy_info(self.ui.list_widget_proxies.currentItem().data(QtCore.Qt.UserRole)))

		# --------------------Account Buttons--------------------
		self.ui.pb_open_login.clicked.connect(self.open_login_window)
		self.ui.pb_save_account.clicked.connect(self.save_account)

		# --------------------Log Buttons--------------------
		self.ui.push_button_export_log.clicked.connect(self.export_log)
		self.ui.push_button_clear_log.clicked.connect(self.clear_log)
		self.ui.line_edit_filter.textChanged.connect(self.filter_log)

		# Show current app version in status bar
		self.statusBar().showMessage('{}'.format(VERSION))

		self.ui.tabWidget.tabBar().setObjectName('tab_widget_tasks')

		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(9, QtWidgets.QHeaderView.Interactive)
		self.ui.table_widget_tasks.horizontalHeader().setSectionResizeMode(10, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_tasks.horizontalHeader().setSectionsClickable(False)
		self.ui.table_widget_tasks.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_tasks.verticalHeader().setSectionsMovable(False)
		self.ui.table_widget_tasks.verticalHeader().setSectionsClickable(False)
		self.ui.table_widget_tasks.setColumnHidden(0, True)

		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		self.ui.tw_accounts.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.horizontalHeader().setSectionsClickable(False)
		self.ui.tw_accounts.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.ui.tw_accounts.verticalHeader().setSectionsMovable(True)
		self.ui.tw_accounts.verticalHeader().setSectionsClickable(False)
		self.ui.tw_accounts.setColumnHidden(0, True)
		# self.ui.table_widget_tasks.verticalHeader().setDefaultSectionSize(50)
		self.ui.table_widget_tasks.horizontalHeader().setSectionsMovable(True)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_proxies.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_proxies.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
		self.ui.table_widget_proxies.horizontalHeader().setSectionsMovable(True)

		self.load_proxy_list()
		self.load_task_list()
		self.load_profile_list()
		self.load_billing_list()
		self.load_combo_box_profiles()
		self.load_combo_box_billing()
		self.load_combo_box_proxies()
		self.load_accounts()

		self.same_as_shipping()
		self.update_proxy_count()
		self.toggle_row_task_type()
		self.toggle_row_task_name()
		self.toggle_row_store()
		self.toggle_row_search_type()
		self.toggle_row_account()
		self.toggle_accounts()
		self.toggle_row_profile()
		self.toggle_row_billing()
		self.toggle_row_proxies()
		self.toggle_proxies()
		self.toggle_row_rotation()
		self.toggle_row_search()
		self.toggle_row_category()
		self.toggle_category()
		self.toggle_row_size()
		self.toggle_size()
		self.toggle_row_color()
		self.toggle_color()
		self.toggle_row_retry()
		self.toggle_row_retry_variance()
		self.toggle_retry_variance()
		self.toggle_row_checkout()
		self.toggle_checkout()
		self.toggle_row_checkout_variance()
		self.toggle_checkout_variance()
		self.toggle_row_qty()
		self.toggle_row_captcha()
		self.new_task()

		# --------------------Toggle Buttons--------------------
		self.toggle_button(self.ui.list_widget_profiles, self.ui.push_button_delete_profile)
		self.toggle_button(self.ui.list_widget_billing, self.ui.push_button_delete_billing)
		self.toggle_button(self.ui.list_widget_proxies, self.ui.push_button_delete_proxies)
		self.ui.group_box_options.toggled.connect(lambda: self.toggle_options(self.ui.group_box_options, self.ui.frame_options))
		self.ui.group_box_log.toggled.connect(lambda: self.toggle_log(self.ui.group_box_log, self.ui.frame_log))
		self.ui.splitter.splitterMoved.connect(self.set_splitter_sizes)

		# --------------------Style Options--------------------
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
		self.ui.pb_step_1.clicked.connect(self.add_to_cart)
		self.ui.pb_step_2.clicked.connect(self.get_basket)
		self.ui.pb_step_3.clicked.connect(self.checkout)
		self.ui.pb_step_4.clicked.connect(self.sign_in_as_guest)
		self.ui.pb_step_5.clicked.connect(self.patch_item_info)
		self.ui.pb_step_6.clicked.connect(self.patch_guest_info)
		self.ui.pb_step_7.clicked.connect(self.load_browser)

	#--------------------Account Functions--------------------

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
		url = 'https://gsp.target.com/gsp/authentications/v1/auth_codes?client_id=ecom-web-1.0.0&state=1585456116676&redirect_uri=https%3A%2F%2Fwww.target.com%2F&assurance_level=M'
		self.login_window.load(QtCore.QUrl(url))
		self.login_window.page().profile().cookieStore().deleteAllCookies()
		self.cookie_store = self.login_window.page().profile().cookieStore()
		self.cookie_store.cookieAdded.connect(self.on_cookie_added)
		self.login_window.show()

	def on_cookie_added(self, cookie):
		self.cookie_jar.insertCookie(cookie)

	#--------------------Test Functions--------------------

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

	def test(self):
		self.render_view.toHtml(self.lol)

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

	#--------------------Mouse Events--------------------

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Control:
			self.ctrl_key = True

	def keyReleaseEvent(self, e):
		if e.key() == QtCore.Qt.Key_Control:
			self.ctrl_key = False

	def eventFilter(self, obj, e):
		if e.type() == QtCore.QEvent.MouseButtonPress and e.button() == QtCore.Qt.LeftButton:
			row = self.ui.table_widget_tasks.rowAt(e.y())
			if row < 0:
				self.ui.table_widget_tasks.selectionModel().clearSelection()
			else:
				if not self.ctrl_key:
					self.ui.table_widget_tasks.selectionModel().clearSelection()

		if e.type() == QtCore.QEvent.MouseButtonRelease and e.button() == QtCore.Qt.LeftButton:
			self.selection_model = self.ui.table_widget_tasks.selectionModel()
			self.task_ids = []
			if self.selection_model.hasSelection():
				self.toggle_delete_task(True)
				for i in self.ui.table_widget_tasks.selectedIndexes()[0::10]:
					task_id = i.data((QtCore.Qt.UserRole))
					self.task_ids.append(task_id)
					self.tasks[task_id].set_font_bold(True)
				if len(self.selection_model.selectedRows()) > 1:
				# if len(self.selection_model.selectedRows()) > 1:
					# Multiple rows selected
					self.enable_mass_edit()
				else:
					# One row selected
					self.disable_mass_edit()
					task = self.tasks[self.task_ids[0]]
					if task.image_large:
						self.ui.label_picture.setPixmap(task.image_large)

					self.load_task_info(task)
				if len(self.task_ids) < self.ui.table_widget_tasks.rowCount():
					self.toggle_task_buttons(len(self.task_ids))
				else:
					self.toggle_task_buttons()
			else:
				# No row(s) selected
				self.new_task()
				self.toggle_task_buttons()
				# self.ui.label_product.setPixmap(self.icon_logo)
				self.ui.label_picture.setPixmap(self.icon_logo)
				for task in self.tasks.values():
					task.set_font_bold(False)
		return QtCore.QObject.event(obj, e)

	#--------------------Toggle Functions--------------------

	def toggle_task_buttons(self, i=None):
		if i:
			self.ui.push_button_start_tasks.setText(f'Start {i}')
			self.ui.push_button_stop_tasks.setText(f'Stop {i}')
			self.ui.push_button_delete_tasks.setText(f'Delete {i}')
		else:
			self.ui.push_button_start_tasks.setText(f'Start All')
			self.ui.push_button_stop_tasks.setText(f'Stop All')
			self.ui.push_button_delete_tasks.setText(f'Delete All')

	def toggle_delete_task(self, toggle):
		self.ui.push_button_delete_task.setEnabled(toggle)

	def toggle_row_task_type(self):
		if self.row_task_type[0].isChecked():
			for item in self.row_task_type[1:]:
				item.setEnabled(True)
			self.row_task_type[2].setCurrentIndex(0)
			if len(self.task_ids) > 1:
				self.row_task_type[3].setEnabled(False)
				self.row_task_type[4].setEnabled(False)
				self.row_task_type[4].setText('1')
			else:
				self.row_task_type[4].setText('1')
		else:
			for item in self.row_task_type[1:]:
				item.setEnabled(False)
			self.row_task_type[2].setCurrentIndex(-1)
			self.row_task_type[4].setText('1')

	def toggle_row_task_name(self):
		if self.row_task_name[0].isChecked():
			for item in self.row_task_name[1:]:
				item.setEnabled(True)
			self.row_task_name[2].clear()
		else:
			for item in self.row_task_name[1:]:
				item.setEnabled(False)
			self.row_task_name[2].clear()

	def toggle_row_store(self):
		if self.row_store[0].isChecked():
			for item in self.row_store[1:]:
				item.setEnabled(True)
			self.row_store[2].setCurrentIndex(0)
		else:
			for item in self.row_store[1:]:
				item.setEnabled(False)
			self.row_store[2].setCurrentIndex(-1)

	def toggle_custom_shopify(self):
		if self.row_store[2].currentText() == 'Custom Shopify':
			self.row_store[2].setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
			self.row_store[3].clear()
			self.row_store[3].show()
			self.row_store[4].show()
			self.row_store[-1].show()
			self.ui.label_tested.setText('Not Tested')
		else:
			self.row_store[2].setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
			self.row_store[3].hide()
			self.row_store[4].hide()
			self.row_store[-1].hide()

	def toggle_row_search_type(self):
		if self.row_search_type[0].isChecked():
			for item in self.row_search_type[1:]:
				item.setEnabled(True)
			self.row_search_type[2].setCurrentIndex(0)
		else:
			for item in self.row_search_type[1:]:
				item.setEnabled(False)
			self.row_search_type[2].setCurrentIndex(-1)

	def toggle_row_account(self):
		if self.row_account[0].isChecked():
			self.row_account[1].setEnabled(True)
			self.row_account[1].setChecked(False)
		else:
			self.row_account[1].setEnabled(False)
			self.row_account[1].setChecked(False)
		self.toggle_accounts()

	def toggle_accounts(self):
		if self.row_account[1].isChecked():
			self.row_account[2].setEnabled(True)
		else:
			self.row_account[2].setEnabled(False)
		self.row_account[2].setCurrentIndex(-1)

	def toggle_row_profile(self):
		if self.row_profile[0].isChecked():
			for item in self.row_profile[1:]:
				item.setEnabled(True)
			# self.row_profile[2].setCurrentIndex(0)
		else:
			for item in self.row_profile[1:]:
				item.setEnabled(False)
		self.row_profile[2].setCurrentIndex(-1)

	def toggle_row_billing(self):
		if self.row_billing[0].isChecked():
			for item in self.row_billing[1:]:
				item.setEnabled(True)
		else:
			for item in self.row_billing[1:]:
				item.setEnabled(False)
		self.row_billing[2].setCurrentIndex(-1)

	def toggle_row_proxies(self):
		if self.row_proxies[0].isChecked():
			self.row_proxies[1].setEnabled(True)
			self.row_proxies[1].setChecked(True)
		else:
			self.row_proxies[1].setEnabled(False)
			self.row_proxies[1].setChecked(False)
		self.toggle_proxies()

	def toggle_proxies(self):
		if self.row_proxies[1].isChecked():
			self.row_proxies[2].setEnabled(True)
			self.load_combo_box_proxies()
			self.row_proxies[2].setCurrentIndex(-1)
		else:
			self.row_proxies[2].setEnabled(False)
			if self.row_proxies[0].isChecked():
				self.row_proxies[2].clear()
				self.row_proxies[2].addItem('localhost')
			else:
				self.row_proxies[2].setCurrentIndex(-1)

	def toggle_row_rotation(self):
		if self.row_rotation[0].isChecked():
			for item in self.row_rotation[1:]:
				item.setEnabled(True)
			self.row_rotation[2].setCurrentIndex(0)
		else:
			for item in self.row_rotation[1:]:
				item.setEnabled(False)
			self.row_rotation[2].setCurrentIndex(-1)

	def toggle_row_search(self):
		if self.row_search[0].isChecked():
			for item in self.row_search[1:]:
				item.setEnabled(True)
		else:
			for item in self.row_search[1:]:
				item.setEnabled(False)
		self.row_search[2].clear()

	def toggle_row_category(self):
		if self.row_category[0].isChecked():
			self.row_category[1].setEnabled(True)
			self.row_category[1].setChecked(True)
		else:
			self.row_category[1].setEnabled(False)
			self.row_category[1].setChecked(False)
		self.toggle_category()

	def toggle_category(self):
		if self.row_category[1].isChecked():
			self.row_category[2].setEnabled(True)
			self.load_combo_box_categories()
		else:
			self.row_category[2].setEnabled(False)
			if self.row_category[0].isChecked():
				self.row_category[2].clear()
				self.row_category[2].addItem('N/A')
			else:
				self.row_category[2].setCurrentIndex(-1)

	def toggle_row_size(self):
		if self.row_size[0].isChecked():
			self.row_size[1].setEnabled(True)
			self.row_size[1].setChecked(True)
		else:
			self.row_size[1].setEnabled(False)
			self.row_size[1].setChecked(False)
		self.toggle_size()

	def toggle_size(self):
		if self.row_size[1].isChecked():
			self.row_size[2].setEnabled(True)
			self.load_combo_box_sizes()
		else:
			self.row_size[2].setEnabled(False)
			if self.row_size[0].isChecked():
				self.row_size[2].clear()
				self.row_size[2].addItem('N/A')
			else:
				self.row_size[2].setCurrentIndex(-1)

	def toggle_row_color(self):
		if self.row_color[0].isChecked():
			self.row_color[1].setEnabled(True)
			self.row_color[1].setChecked(True)
		else:
			self.row_color[1].setEnabled(False)
			self.row_color[1].setChecked(False)

	def toggle_color(self):
		if self.row_color[1].isChecked():
			self.row_color[2].setEnabled(True)
		else:
			self.row_color[2].setEnabled(False)
			self.row_color[2].clear()

	def toggle_row_retry(self):
		if self.row_retry[0].isChecked():
			self.row_retry[1].setEnabled(True)
			self.row_retry[2].setEnabled(True)
			self.row_retry[3].setEnabled(True)
			self.row_retry[-1].setEnabled(True)
		else:
			self.row_retry[1].setEnabled(False)
			self.row_retry[2].setEnabled(False)
			self.row_retry[2].clear()
			self.row_retry[3].setEnabled(False)
			self.row_retry[-1].setEnabled(False)

	def toggle_row_retry_variance(self):
		if self.row_retry_variance[0].isChecked():
			self.row_retry_variance[1].setEnabled(True)
			self.row_retry_variance[1].setChecked(True)
		else:
			self.row_retry_variance[1].setEnabled(False)
			self.row_retry_variance[1].setChecked(False)

	def toggle_retry_variance(self):
		if self.row_retry_variance[1].isChecked():
			self.row_retry_variance[2].setEnabled(True)
			self.row_retry_variance[3].setEnabled(True)
		else:
			self.row_retry_variance[2].setEnabled(False)
			self.row_retry_variance[2].clear()
			self.row_retry_variance[3].setEnabled(False)

	def toggle_row_checkout(self):
		if self.row_checkout[0].isChecked():
			self.row_checkout[1].setEnabled(True)
			self.row_checkout[1].setChecked(True)
			self.row_checkout[-1].setEnabled(True)
		else:
			self.row_checkout[1].setEnabled(False)
			self.row_checkout[1].setChecked(False)
			self.row_checkout[-1].setEnabled(False)

	def toggle_checkout(self):
		if self.row_checkout[1].isChecked():
			self.row_checkout[2].setEnabled(True)
			self.row_checkout[3].setEnabled(True)
		else:
			self.row_checkout[2].setEnabled(False)
			self.row_checkout[2].clear()
			self.row_checkout[3].setEnabled(False)

	def toggle_row_checkout_variance(self):
		if self.row_checkout_variance[0].isChecked():
			self.row_checkout_variance[1].setEnabled(True)
			self.row_checkout_variance[1].setChecked(True)
		else:
			self.row_checkout_variance[1].setEnabled(False)
			self.row_checkout_variance[1].setChecked(False)

	def toggle_checkout_variance(self):
		if self.row_checkout_variance[1].isChecked():
			self.row_checkout_variance[2].setEnabled(True)
			self.row_checkout_variance[3].setEnabled(True)
		else:
			self.row_checkout_variance[2].setEnabled(False)
			self.row_checkout_variance[2].clear()
			self.row_checkout_variance[3].setEnabled(False)

	def toggle_row_qty(self):
		if self.row_qty[0].isChecked():
			self.row_qty[1].setEnabled(True)
			self.row_qty[2].setEnabled(True)
			self.row_qty[2].setCurrentIndex(0)
		else:
			self.row_qty[1].setEnabled(False)
			self.row_qty[2].setEnabled(False)
			self.row_qty[2].setCurrentIndex(-1)

	def toggle_row_captcha(self):
		if self.row_captcha[0].isChecked():
			self.row_captcha[1].setEnabled(True)
			self.row_captcha[1].setCheckState(QtCore.Qt.PartiallyChecked)
		else:
			self.row_captcha[1].setEnabled(False)
			self.row_captcha[1].setChecked(False)

	# def toggle_captcha(self):
	# 	if self.row_captcha[1].isEnabled():
	# 		if self.row_captcha[1].checkState() == QtCore.Qt.Unchecked:
	# 			self.row_captcha[2].setText('The Gecko App will ignore captcha')
	# 		elif self.row_captcha[1].checkState() == QtCore.Qt.PartiallyChecked:
	# 			self.row_captcha[2].setText('The Gecko App will detect captcha')
	# 		elif self.row_captcha[1].checkState() == QtCore.Qt.Checked:
	# 			self.row_captcha[2].setText('The Gecko App will require captcha')
	# 	else:
	# 		self.row_captcha[2].clear()

	def toggle_mask_proxies(self):
		for task in self.tasks.values():
			task.check_box_mask_proxy.setCheckState(self.ui.check_box_mask_proxies.checkState())
			# task.mask_proxies(self.ui.check_box_mask_proxies.checkState())
		self.ui.table_widget_tasks.resizeColumnToContents(7)

	#--------------------Captcha Window--------------------

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

	#--------------------Custom Signal Functions--------------------

	def update_task_status(self, message, item):
		row = self.ui.table_widget_tasks.row(item)
		self.ui.table_widget_tasks.item(row, 8).setText(message)
		# self.ui.table_widget_tasks.resizeColumnToContents(8)

	def update_delay(self, message, item):
		row = self.ui.table_widget_tasks.row(item)
		self.ui.table_widget_tasks.item(row, 9).setText(message)

	def update_task_title(self, title, item):
		row = self.ui.table_widget_tasks.row(item)
		self.ui.table_widget_tasks.item(row, 4).setText(title)

	def update_task_log(self, message):
		self.post_to_log(message)

	#--------------------Core Functions--------------------

	def load_types(self, index):
		self.ui.combo_box_search_type.clear()
		self.ui.combo_box_task_type.clear()
		data = self.ui.combo_box_store.currentData(QtCore.Qt.UserRole)
		if data:
			# Search type
			if 'k' in data:
				self.ui.combo_box_search_type.addItem('Keywords')
			if 'd' in data:
				self.ui.combo_box_search_type.addItem('Direct Link')
			if 'v' in data:
				self.ui.combo_box_search_type.addItem('Variant')
			# Task type
			if 'n' in data:
				self.ui.combo_box_task_type.addItem('Normal')
			if 'm' in data:
				self.ui.combo_box_task_type.addItem('Monitor')
			if 'r' in data:
				self.ui.combo_box_task_type.addItem('Restock')

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

	#--------------------Group Box Tasks Functions--------------------

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
			self.post_to_log('Deleted all tasks successfully')
			self.task_ids = []

	def open_captcha(self):
		pass

	#--------------------Group Box Log Functions--------------------

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

	#--------------------Tab Widget Task Functions--------------------

	def load_task_list(self):
		self.ui.table_widget_tasks.setRowCount(0)
		data = self.tgadb.get_all_tasks()
		if data:
			self.create_task(data)
		else:
			print('there is no data')

	def edit_tasks(self, data):
		print(type(data))
		print(data)

	def create_task(self, data, task_id=None, update=False):
		if task_id:
			row = self.ui.table_widget_tasks.row(self.tasks[task_id].widget_task_id)
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, ab, ac, ad in data:
			profile_data = self.tgadb.get_profile(k)
			billing_data = self.tgadb.get_billing(l)
			if j is not None:
				account_data = self.tgadb.get_account(j)
				for da, db, dc, dd in account_data:
					account = Account(da, db, dc, dd)
			else:
				account = Account()
			if n is not None:
				proxy_data = self.tgadb.get_proxy(n)
				for da, db, dc in proxy_data:
					proxy = Proxy(da, db, dc)
			else:
				proxy = Proxy()
			for ba, bb, bc, bd, be, bf, bg, bh, bi, bj, bk, bl, bm, bn, bo, bp, bq in profile_data:
				profile = Profile(ba, bb, bc, bd, be, bf, bg, bh, bi, bj, bk, bl, bm, bn, bo, bp, bq)
			for ca, cb, cc, cd ,ce, cf, cg, ch in billing_data:
				billing = Billing(ca, cb, cc, cd, ce, cf, cg, ch)
			# for da, db, dc, dd in account_data:
			# 	account = Account(da, db, dc, dd)

			task = Task(a, b, c, d, e, f, g, h, i, account, profile, billing, m, proxy, o, p, q, r, s, t, u, v, w, x, y, z, aa, ab, ac, ad)
			task.update_log.connect(self.update_task_log)
			task.button_start.clicked.connect(task.start_task)
			task.button_stop.clicked.connect(task.stop_task)
			task.button_delete.clicked.connect(task.delete_task)
			task.started.connect(task.enable_stop)
			task.finished.connect(task.enable_start)
			task.delete.connect(self.delete_task)
			task.error_delete.connect(self.error_on_delete_task)
			task.request_captcha.connect(self.request_captcha)
			task.poll_response.connect(self.poll_response)
			# task.poll_token.connect(self.get_token_from_queue)
			task.request_abort.connect(self.request_abort)
			task.update_proxy_label.connect(self.update_proxy)
			task.load_browser.connect(self.load_task_browser)
			task.update_status.connect(self.update_task_status)
			task.update_delay.connect(self.update_delay)
			task.update_title.connect(self.update_task_title)
			# task.update_title.connect(self.update_title)
			# task.update_proxy.connect(self.update_proxy)
			# task.product_updated.connect(self.update_product)
			# task.update_image.connect(self.update_image)
			# task.update_size.connect(self.update_size)
			task.send_cookies.connect(self.set_cookies)
			# task.send_url.connect(self.render_js)
			if update:
				self.update_task(task, row)
			else:
				self.add_task(task)
			self.tasks[a] = task

	def add_task(self, task):
		row = self.ui.table_widget_tasks.rowCount()
		self.ui.table_widget_tasks.insertRow(row)
		self.ui.table_widget_tasks.setItem(row, 0, task.widget_task_id)
		self.ui.table_widget_tasks.setItem(row, 1, task.widget_task_type)
		self.ui.table_widget_tasks.setItem(row, 2, task.widget_task_name)
		# self.ui.table_widget_tasks.setCellWidget(row, 2, task.widget_task_name)
		self.ui.table_widget_tasks.setItem(row, 3, task.widget_profile)
		self.ui.table_widget_tasks.setItem(row, 4, task.widget_product)
		self.ui.table_widget_tasks.setCellWidget(row, 5, task.widget_image)
		self.ui.table_widget_tasks.setItem(row, 6, task.widget_size)
		self.ui.table_widget_tasks.setItem(row, 7, task.widget_proxy)
		self.ui.table_widget_tasks.setItem(row, 8, task.widget_status)
		self.ui.table_widget_tasks.setItem(row, 9, task.widget_delay)
		self.ui.table_widget_tasks.setCellWidget(row, 10, task.actions)
		# self.ui.table_widget_tasks.resizeColumnsToContents()
		self.ui.table_widget_tasks.resizeColumnToContents(10)

	def update_task(self, task, row):
		# get row of current modified task
		# row = self.ui.table_widget_tasks.row(old.widget_task_id)
		self.ui.table_widget_tasks.setItem(row, 0, task.widget_task_id)
		self.ui.table_widget_tasks.setItem(row, 1, task.widget_task_type)
		self.ui.table_widget_tasks.setItem(row, 2, task.widget_task_name)
		# self.ui.table_widget_tasks.setCellWidget(row, 2, task.widget_task_name)
		self.ui.table_widget_tasks.setItem(row, 3, task.widget_profile)
		self.ui.table_widget_tasks.setItem(row, 4, task.widget_product)
		self.ui.table_widget_tasks.setCellWidget(row, 5, task.widget_image)
		self.ui.table_widget_tasks.setItem(row, 6, task.widget_size)
		self.ui.table_widget_tasks.setItem(row, 7, task.widget_proxy)
		self.ui.table_widget_tasks.setItem(row, 8, task.widget_status)
		self.ui.table_widget_tasks.setItem(row, 9, task.widget_delay)
		self.ui.table_widget_tasks.setCellWidget(row, 10, task.actions)
		# self.ui.table_widget_tasks.viewport().update()

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

	def load_task_info(self, task):
		if self.ui.table_widget_tasks.selectionModel().hasSelection():
			# print(self.ui.table_widget_tasks.selectedIndexes()[0].data(QtCore.Qt.UserRole))
			# task = self.tasks[task_id]
			self.ui.line_edit_task_name.setText(str(task.task_name))
			self.ui.line_edit_task_qty.setText('1')
			self.ui.combo_box_task_type.setCurrentIndex(self.ui.combo_box_task_type.findText(task.task_type))
			self.ui.combo_box_store.setCurrentIndex(self.ui.combo_box_store.findText(task.store_name))
			self.ui.combo_box_qty.setCurrentIndex(self.ui.combo_box_qty.findText(str(task.qty)))
			self.ui.check_box_captcha.setCheckState(task.check_box_captcha)
			self.ui.combo_box_search_type.setCurrentIndex(self.ui.combo_box_search_type.findText(task.search_type))
			self.ui.line_edit_search.setText(str(task.search))
			self.ui.check_box_account.setCheckState(task.check_box_account)
			if task.account.account_id:
				self.ui.combo_box_accounts.setCurrentIndex(self.ui.combo_box_accounts.findData(task.account.account_id))
			self.ui.combo_box_profiles.setCurrentIndex(self.ui.combo_box_profiles.findData(task.profile.profile_id))
			self.ui.combo_box_billing.setCurrentIndex(self.ui.combo_box_billing.findData(task.billing.billing_id))
			self.ui.check_box_proxies.setCheckState(task.check_box_proxies)
			if task.proxy_profile.proxy_id:
				self.ui.combo_box_proxies.setCurrentIndex(self.ui.combo_box_proxies.findData(task.proxy_profile.proxy_id))
			self.ui.combo_box_rotation.setCurrentIndex(self.ui.combo_box_rotation.findText(task.rotation))
			self.ui.check_box_category.setCheckState(task.check_box_category)
			if self.ui.check_box_category.checkState() == QtCore.Qt.Checked:
				self.ui.combo_box_category.setCurrentIndex(self.ui.combo_box_category.findText(task.category))
			self.ui.check_box_size.setCheckState(task.check_box_size)
			if self.ui.check_box_size.checkState() == QtCore.Qt.Checked:
				self.ui.combo_box_size.setCurrentIndex(self.ui.combo_box_size.findText(task.size))
			self.ui.check_box_color.setCheckState(task.check_box_color)
			if self.ui.check_box_color.checkState() == QtCore.Qt.Checked:
				self.ui.line_edit_color.setText(str(task.color))
			self.ui.line_edit_retry_delay.setText(str(task.retry_delay))
			self.ui.check_box_retry_variance.setCheckState(task.check_box_retry_var)
			if self.ui.check_box_retry_variance.checkState() == QtCore.Qt.Checked:
				self.ui.line_edit_retry_variance.setText(str(task.retry_var))
			self.ui.check_box_checkout_delay.setCheckState(task.check_box_checkout_delay)
			if self.ui.check_box_checkout_delay.checkState() == QtCore.Qt.Checked:
				self.ui.line_edit_checkout_delay.setText(str(task.checkout_delay))
			self.ui.check_box_checkout_variance.setCheckState(task.check_box_checkout_var)
			if self.ui.check_box_checkout_variance.checkState() == QtCore.Qt.Checked:
				self.ui.line_edit_checkout_variance.setText(str(task.checkout_var))

	def new_task(self):
		# self.ui.table_widget_tasks.clearSelection()
		# self.ui.table_widget_tasks.selectionModel().clear()
		# self.task_ids = []
		self.toggle_delete_task(False)
		self.disable_mass_edit()
		self.clear_task_fields()
		self.ui.table_widget_tasks.selectionModel().clearSelection()
		self.task_ids = []

	def clear_task_fields(self):
		self.ui.combo_box_task_type.setCurrentIndex(0)
		self.ui.combo_box_store.setCurrentIndex(-1)
		self.ui.combo_box_search_type.setCurrentIndex(0)
		self.ui.line_edit_search.clear()
		self.ui.line_edit_task_name.clear()
		self.ui.line_edit_task_qty.setText('1')
		self.ui.check_box_account.setChecked(False)
		self.ui.combo_box_profiles.setCurrentIndex(-1)
		self.ui.combo_box_billing.setCurrentIndex(-1)
		self.ui.combo_box_accounts.setCurrentIndex(-1)
		self.ui.check_box_proxies.setChecked(False)
		self.toggle_proxies()
		self.ui.combo_box_rotation.setCurrentIndex(0)
		self.ui.check_box_category.setChecked(False)
		self.ui.check_box_size.setChecked(False)
		self.ui.check_box_color.setChecked(False)
		self.ui.check_box_captcha.setCheckState(QtCore.Qt.Unchecked)
		self.ui.combo_box_qty.setCurrentIndex(0)
		self.ui.line_edit_retry_delay.clear()
		self.ui.check_box_retry_variance.setChecked(False)
		self.ui.check_box_checkout_delay.setChecked(False)
		self.ui.check_box_checkout_variance.setChecked(False)

	def save_task(self):
		items = {
			'line_edit_task_name': self.ui.line_edit_task_name.text(),
			'combo_box_task_type': self.ui.combo_box_task_type.currentText(),
			'combo_box_store': self.ui.combo_box_store.currentText(),
			'combo_box_qty': self.ui.combo_box_qty.currentText(),
			'check_box_captcha': self.ui.check_box_captcha.checkState(),
			'combo_box_search_type': self.ui.combo_box_search_type.currentText(),
			'line_edit_search': self.ui.line_edit_search.text(),
			'check_box_account': self.ui.check_box_account.checkState(),
			'combo_box_accounts': self.ui.combo_box_accounts.currentData(QtCore.Qt.UserRole),
			'combo_box_profiles': self.ui.combo_box_profiles.currentData(QtCore.Qt.UserRole),
			'combo_box_billing': self.ui.combo_box_billing.currentData(QtCore.Qt.UserRole),
			'check_box_proxies': self.ui.check_box_proxies.checkState(),
			'combo_box_proxies': self.ui.combo_box_proxies.currentData(QtCore.Qt.UserRole),
			'combo_box_rotation': self.ui.combo_box_rotation.currentText(),
			'check_box_category': self.ui.check_box_category.checkState(),
			'combo_box_category': self.ui.combo_box_category.currentText(),
			'check_box_size': self.ui.check_box_size.checkState(),
			'combo_box_size': self.ui.combo_box_size.currentText(),
			'check_box_color': self.ui.check_box_color.checkState(),
			'line_edit_color': self.ui.line_edit_color.text(),
			'line_edit_retry_delay': self.ui.line_edit_retry_delay.text(),
			'check_box_retry_variance': self.ui.check_box_retry_variance.checkState(),
			'line_edit_retry_variance': self.ui.line_edit_retry_variance.text(),
			'check_box_checkout_delay': self.ui.check_box_checkout_delay.checkState(),
			'line_edit_checkout_delay': self.ui.line_edit_checkout_delay.text(),
			'check_box_checkout_variance': self.ui.check_box_checkout_variance.checkState(),
			'line_edit_checkout_variance': self.ui.line_edit_checkout_variance.text(),
			'base_url': self.shopify['base_url'],
			'api_key': self.shopify['api_key']
		}
		tasks = len(self.task_ids)
		task_qty = int(self.ui.line_edit_task_qty.text())
		if tasks < 1:
			# Create new task
			base_name = items['line_edit_task_name']
			i = 0
			while i < task_qty:
				if i > 0:
					items['line_edit_task_name'] = f'{base_name} ({i})'
				self.tgadb.save_task(items)
				data = self.tgadb.get_recent_task()
				self.create_task(data)
				i += 1
			self.new_task()
		elif tasks == 1:
			# Update a task
			base_name = items['line_edit_task_name']
			i = 0
			while i < task_qty:
				if i > 0:
					items['line_edit_task_name'] = f'{base_name} ({i})'
					self.tgadb.save_task(items)
					data = self.tgadb.get_recent_task()
					self.create_task(data)
				task_id = self.task_ids[0]
				self.tgadb.save_task(items, task_id)
				data = self.tgadb.get_task(task_id)
				self.create_task(data, task_id=task_id, update=True)
				i += 1
			self.new_task()
		else:
			# Mass edit
			fields = self.check_mass_edit_fields()
			if fields:
				for task_id in self.task_ids:
					for key, value in fields.items():
						self.tgadb.update_task(key, value, task_id)
					data = self.tgadb.get_task(task_id)
					self.create_task(data, task_id=task_id, update=True)
				self.new_task()
			else:
				self.confirmation_dialog('Error', 'One or more fields are empty.')

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
			cb.setEnabled(True)
			cb.show()

	def disable_mass_edit(self):
		for cb in self.cbe_items:
			cb.setChecked(True)
			self.toggle_row_task_type()
			cb.setEnabled(False)
			cb.hide()

	def load_combo_box_profiles(self):
		self.ui.combo_box_profiles.clear()
		data = self.tgadb.get_all_profiles()
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q in data:
			self.ui.combo_box_profiles.addItem(b, a)

	def load_combo_box_billing(self):
		self.ui.combo_box_billing.clear()
		data = self.tgadb.get_all_billing()
		for a, b, c, d, e, f, g, h in data:
			self.ui.combo_box_billing.addItem(b, a)

	def load_combo_box_proxies(self):
		self.ui.combo_box_proxies.clear()
		data = self.tgadb.get_all_proxies()
		for a, b, c in data:
			self.ui.combo_box_proxies.addItem(b, a)

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

	#--------------------Tab Widget Profile Functions--------------------

	def load_profile_list(self):
		data = self.tgadb.get_all_profiles()
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q in data:
			item = QtWidgets.QListWidgetItem(b)
			item.setData(QtCore.Qt.UserRole, a)
			self.ui.list_widget_profiles.addItem(item)

	def load_profile_info(self, profile_id):
		data = self.tgadb.get_profile(profile_id)
		for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q in data:
			self.ui.line_edit_profile_name.setText(b)
			self.ui.line_edit_first_name.setText(c)
			self.ui.line_edit_last_name.setText(d)
			self.ui.line_edit_email.setText(e)
			self.ui.line_edit_phone.setText(f)
			self.ui.check_box_same_as_shipping.setCheckState(g)
			self.ui.line_edit_shipping_address.setText(h)
			self.ui.line_edit_shipping_address_2.setText(i)
			self.ui.line_edit_shipping_city.setText(j)
			self.ui.combo_box_shipping_state.setCurrentIndex(self.ui.combo_box_shipping_state.findText(k))
			self.ui.line_edit_shipping_zip.setText(l)
			self.ui.line_edit_billing_address.setText(m)
			self.ui.line_edit_billing_address_2.setText(n)
			self.ui.line_edit_billing_city.setText(o)
			self.ui.combo_box_billing_state.setCurrentIndex(self.ui.combo_box_billing_state.findText(p))
			self.ui.line_edit_billing_zip.setText(q)

	def new_profile(self):
		for item in self.profile_items:
			if type(item) is QtWidgets.QLineEdit:
				item.clear()
			elif type(item) is QtWidgets.QComboBox:
				item.setCurrentIndex(0)
			elif type(item) is QtWidgets.QCheckBox:
				item.setChecked(True)
		self.ui.list_widget_profiles.clearSelection()
		self.ui.list_widget_profiles.selectionModel().clear()

	def save_profile(self):
		item = self.ui.list_widget_profiles.currentItem()
		items = {
			'profile_name': self.ui.line_edit_profile_name.text(),
			'first_name': self.ui.line_edit_first_name.text(),
			'last_name': self.ui.line_edit_last_name.text(),
			'email': self.ui.line_edit_email.text(),
			'phone': self.ui.line_edit_phone.text(),
			'same_as_shipping': self.ui.check_box_same_as_shipping.checkState(),
			'shipping_address': self.ui.line_edit_shipping_address.text(),
			'shipping_address_2': self.ui.line_edit_shipping_address_2.text(),
			'shipping_city': self.ui.line_edit_shipping_city.text(),
			'shipping_state': self.ui.combo_box_shipping_state.currentText(),
			'shipping_zip': self.ui.line_edit_shipping_zip.text(),
			'billing_address': self.ui.line_edit_billing_address.text(),
			'billing_address_2': self.ui.line_edit_billing_address_2.text(),
			'billing_city': self.ui.line_edit_billing_city.text(),
			'billing_state': self.ui.combo_box_billing_state.currentText(),
			'billing_zip': self.ui.line_edit_billing_zip.text()
		}
		if self.validate_fields(self.profile_items):
			try:
				if item:
					self.tgadb.save_profile(items, item.data(QtCore.Qt.UserRole))
				else:
					self.tgadb.save_profile(items)
			except Exception as e:
				self.post_to_log('Error saving profile [{}]'.format(str(e)))
			else:
				self.post_to_log('Profile [{}] saved successfully'.format(items['profile_name']))
				self.new_profile()
				# update list widget profiles (addItem)
				self.ui.list_widget_profiles.clear()
				self.ui.list_widget_profiles.clearSelection()
				self.ui.list_widget_profiles.selectionModel().clear()
				self.load_profile_list()
				# update combo box profile
				self.load_combo_box_profiles()
		else:
			self.post_to_log('One or more fields are empty')

	def delete_profile(self, profile_id):
		# delete from database
		try:
			profile_name = self.ui.list_widget_profiles.currentItem().text()
			self.tgadb.delete_profile(profile_id)
		except Exception as e:
			self.post_to_log('Error deleting profile [{}]'.format(str(e)))
		else:
			# clear fields
			self.new_profile()
			# update list widget profiles
			self.ui.list_widget_profiles.clear()
			self.load_profile_list()
			# clear selections
			self.ui.list_widget_profiles.clearSelection()
			self.ui.list_widget_profiles.selectionModel().clear()
			# post to log
			self.post_to_log('Deleted profile [{}] successfully'.format(profile_name))
			# update combo box billing profile
			self.load_combo_box_billing()

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

	# def live_copy_shipping(self, pair):
	# 	if self.ui.check_box_same_as_shipping.isChecked():
	# 		pair[0].setText(pair[1].text())

	# def load_combo_box_billing(self):
	# 	self.ui.combo_box_billing_profile.clear()
	# 	data = self.tgadb.get_all_billing()
	# 	for a, b, c, d, e, f, g, h in data:
	# 		self.ui.combo_box_billing_profile.addItem(b, a)

	#--------------------Tab Widget Billing Functions--------------------

	def load_billing_list(self):
		data = self.tgadb.get_all_billing()
		for a, b, c, d, e, f, g, h in data:
			item = QtWidgets.QListWidgetItem(b)
			item.setData(QtCore.Qt.UserRole, a)
			self.ui.list_widget_billing.addItem(item)

	def load_billing_info(self, billing_id):
		data = self.tgadb.get_billing(billing_id)
		for a, b, c, d, e, f, g, h in data:
			self.ui.line_edit_billing_name.setText(b)
			self.ui.line_edit_name_on_card.setText(c)
			self.ui.combo_box_card_type.setCurrentIndex(self.ui.combo_box_card_type.findText(d))
			self.ui.line_edit_card_number.setText(e)
			self.ui.combo_box_exp_month.setCurrentIndex(self.ui.combo_box_exp_month.findText(f))
			self.ui.combo_box_exp_year.setCurrentIndex(self.ui.combo_box_exp_year.findText(g))
			self.ui.line_edit_cvv.setText(h)

	def new_billing_profile(self):
		for item in self.billing_items:
			if type(item) is QtWidgets.QLineEdit:
				item.clear()
			elif type(item) is QtWidgets.QComboBox:
				item.setCurrentIndex(0)
		self.ui.list_widget_billing.clearSelection()
		self.ui.list_widget_billing.selectionModel().clear()

	def save_billing_profile(self):
		item = self.ui.list_widget_billing.currentItem()
		items = {
			'billing_name': self.ui.line_edit_billing_name.text(),
			'name_on_card': self.ui.line_edit_name_on_card.text(),
			'card_type': self.ui.combo_box_card_type.currentText(),
			'card_number': self.ui.line_edit_card_number.text(),
			'exp_month': self.ui.combo_box_exp_month.currentText(),
			'exp_year': self.ui.combo_box_exp_year.currentText(),
			'cvv': self.ui.line_edit_cvv.text()
		}
		# validate items
		if self.validate_fields(self.billing_items):
			try:
				if item:
					self.tgadb.save_billing(items, item.data(QtCore.Qt.UserRole))
				else:
					self.tgadb.save_billing(items)
			except Exception as e:
				self.post_to_log('Error saving billing profile [{}]'.format(str(e)))
			else:
				if item:
					self.post_to_log('Billing profile [{}] updated successfully'.format(items['billing_name']))
				else:
					self.post_to_log('Billing profile [{}] saved successfully'.format(items['billing_name'])) # post to console/log
				# clear fields
				self.new_billing_profile()
				# update list widget billing (addItem)
				self.ui.list_widget_billing.clear()
				self.load_billing_list()
				self.ui.list_widget_billing.clearSelection()
				self.ui.list_widget_billing.selectionModel().clear()
				# update combo box billing profile
				self.load_combo_box_billing()
		else:
			self.post_to_log('One or more fields are empty')

	def delete_billing_profile(self, billing_id):
		# delete from database
		try:
			billing_name = self.ui.list_widget_billing.currentItem().text()
			self.tgadb.delete_billing(billing_id)
		except Exception as e:
			self.post_to_log('Error deleting billing profile [{}]'.format(str(e)))
		else:
			# clear fields
			self.new_billing_profile()
			self.ui.list_widget_billing.clear()
			# clear selections
			self.ui.list_widget_billing.clearSelection()
			self.ui.list_widget_billing.selectionModel().clear()
			self.load_billing_list()
			# post to log
			self.post_to_log('Deleted billing profile [{}] successfully'.format(billing_name))
			# update combo box billing profile
			self.load_combo_box_billing()

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

	#--------------------Tab Widget Proxies Functions--------------------

	def load_proxy_list(self):
		data = self.tgadb.get_all_proxies()
		if data:
			for a, b, c in data:
				proxy = Proxy(a, b, c)
				# print(type(proxy.proxy_id))
				self.proxies[proxy.proxy_id] = proxy
				item = QtWidgets.QListWidgetItem(proxy.proxy_name)
				item.setData(QtCore.Qt.UserRole, proxy.proxy_id)
				self.ui.list_widget_proxies.addItem(item)
				# proxy_id = a
				# proxy_name = b
				# proxies = c
				# item = QtWidgets.QListWidgetItem(proxy_name)
				# item.setData(QtCore.Qt.UserRole, proxy_id)
				# self.ui.list_widget_proxies.addItem(item)
		else:
			print('there is no data')

	def load_proxy_info(self, proxy_id):
		data = self.tgadb.get_proxy(proxy_id)
		if data:
			for a, b, c in data:
				self.proxy = Proxy(a, b, c)
				# proxy_id = a
				# proxy_name = b
				# proxies = c
			self.ui.line_edit_proxy_name.setText(self.proxy.proxy_name)
			self.ui.plain_text_edit_proxies.setPlainText(self.proxy.proxies)

			# clear rows before inserting
			# self.ui.table_widget_proxies.setRowCount(0)
			# row = 0
			# for item in self.proxy.proxies.split('\n'):
			# 	self.ui.table_widget_proxies.insertRow(self.ui.table_widget_proxies.rowCount())
			# 	self.ui.table_widget_proxies.setItem(row, 0, QtWidgets.QTableWidgetItem(item))
			# 	self.ui.table_widget_proxies.setCellWidget(row, 2, self.proxy.button_widgets[row])
			# 	# print(proxy.buttons[row])
			# 	row += 1
		else:
			print('there is no data')

	def new_proxy_profile(self):
		for item in self.proxy_items:
			if type(item) is QtWidgets.QLineEdit:
				item.clear()
			elif type(item) is QtWidgets.QComboBox:
				item.setCurrentIndex(-1)
			elif type(item) is QtWidgets.QCheckBox:
				item.setChecked(True)
			elif type(item) is QtWidgets.QPlainTextEdit:
				item.clear()
		self.ui.list_widget_proxies.clearSelection()
		self.ui.list_widget_proxies.selectionModel().clear()
		# clear rows
		self.ui.table_widget_proxies.setRowCount(0)

	def save_proxy_profile(self):
		item = self.ui.list_widget_proxies.currentItem()
		items = {
			'proxy_name': self.ui.line_edit_proxy_name.text(),
			'proxies': self.ui.plain_text_edit_proxies.toPlainText()
		}
		# validate items
		if self.validate_fields(self.proxy_items):
			try:
				if item:
					self.tgadb.save_proxy(items, item.data(QtCore.Qt.UserRole))
				else:
					self.tgadb.save_proxy(items)
			except Exception as e:
				self.post_to_log('Error saving proxy profile [{}]'.format(str(e)))
			else:
				if item:
					self.post_to_log('Proxy profile [{}] updated successfully'.format(items['proxy_name']))
				else:
					self.post_to_log('Proxy profile [{}] saved successfully'.format(items['proxy_name'])) # post to console/log
				# clear fields
				self.new_proxy_profile()
				# update list widget proxies (addItem)
				self.ui.list_widget_proxies.clear()
				self.ui.list_widget_proxies.clearSelection()
				self.ui.list_widget_proxies.selectionModel().clear()
				self.load_proxy_list()
				# update combo box proxies profile
				self.load_combo_box_proxies()
		else:
			self.post_to_log('One or more fields are empty')

	def delete_proxy_profile(self, proxy_id):
		# delete from database
		try:
			proxy_name = self.ui.list_widget_proxies.currentItem().text()
			self.tgadb.delete_proxy(proxy_id)
		except Exception as e:
			self.post_to_log('Error deleting proxy profile [{}]'.format(str(e)))
		else:
			# clear fields
			self.new_proxy_profile()
			self.ui.list_widget_proxies.clear()
			# clear selections
			self.ui.list_widget_proxies.clearSelection()
			self.ui.list_widget_proxies.selectionModel().clear()
			self.load_proxy_list()
			# post to log
			self.post_to_log('Deleted proxy profile [{}] successfully'.format(proxy_name))
			# update combo box proxy profile
			self.load_combo_box_proxies()

	def delete_all_proxy_profiles(self):
		# prompt dialog for "are you sure" before deleting
		if self.confirmation_dialog('Please Confirm', 'Are you sure you want to delete all proxies?'):
			try:
				self.tgadb.delete_all_proxies()
			except Exception as e:
				self.post_to_log('Error deleting all proxy profiles [{}]'.format(str(e)))
			else:
				# post to log
				self.post_to_log('Deleted all proxy profiles successfully')
				# clear fields
				self.new_proxy_profile()
				self.ui.list_widget_proxies.clear()
				# clear selections
				self.ui.list_widget_proxies.clearSelection()
				self.ui.list_widget_proxies.selectionModel().clear()
				# update combo box billing profile
				self.load_combo_box_proxies()
		else:
			print('Operation aborted')

	def import_proxies(self):
		# print(type(self.open_file()))
		self.ui.plain_text_edit_proxies.setPlainText(self.open_file())

	def update_proxy_count(self):
		i = self.ui.plain_text_edit_proxies.toPlainText().splitlines()
		self.ui.label_proxy_count.setText(str(len(i)))

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