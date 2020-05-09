from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtNetwork

from bs4 import BeautifulSoup

import requests
import json
import time

import gecko_utils

# VERSION 0.1
class HyperXGaming(QObject):

	update_status = pyqtSignal(str)
	update_title = pyqtSignal(str)
	update_image = pyqtSignal(str)
	
	request_captcha = pyqtSignal()
	poll_response = pyqtSignal()

	headers = {
		'accept': '*/*',
		# 'accept-encoding': 'gzip, deflate, br',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'host': 'www.hyperxgaming.com',
		'origin': 'https://www.hyperxgaming.com',
		'pragma': 'no-cache',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
		'x-requested-with': 'XMLHttpRequest'
	}

	def __init__(self, search, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.proxy = None
		self.sku = search
		self.profile = profile
		self.billing = billing

		# Webhook info
		self.store = 'https://www.hyperxgaming.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		self.abort = False
		self.stripe_key = 'pk_live_GiSktffRI3h9Z05kpLUWEIVi'

		self.status = 'Ready'

		self.current_step = 0

		self.steps = [
			self.add_to_cart,
			self.get_stripe_token
		]

	def add_to_cart(self):
		self.current_step = 0
		self.status = 'Adding to cart'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.hyperxgaming.com/us/shop/basket'
		payload = {
			'partNumber': 'HX-MC005B',
			'quantity': self.qty
		}
		try:
			r = self.s.post(url, headers=self.headers, data=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True
		elif int(str(r.status_code)[0]) == 4:
			print(r.text)
			self.status = 'Too many requests'
		elif r.status_code[0] == 5:
			self.status = 'Server error'
		else:
			self.status = 'Error carting'

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def get_stripe_token(self):
		self.current_step = 1
		self.status = 'Tokenizing'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://api.stripe.com/v1/tokens'
		payload = {
			'card[name]': self.billing.name_on_card,
			'card[address_line1]': self.profile.billing_address,
			'card[address_line2]': self.profile.billing_address_2,
			'card[address_city]': self.profile.billing_city,
			'card[address_state]': self.profile.billing_state,
			'card[address_zip]': self.profile.billing_zip,
			'card[address_country]': 'US',
			'card[number]': self.billing.card_number,
			'card[cvc]': self.billing.cvv,
			'card[exp_month]': self.billing.exp_month,
			'card[exp_year]': self.billing.exp_year,
			# 'guid': '',
			# 'muid': '',
			# 'sid': '',
			'payment_user_agent': 'stripe.js/8b044688;+stripe-js-v3/8b044688',
			'time_on_page': '189619',
			'referrer': 'https://www.hyperxgaming.com/us/shop/order/checkout',
			'key': self.stripe_key
		}
		try:
			r = self.s.post(url, headers=self.headers, data=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True
		elif int(str(r.status_code)[0]) == 4:
			print(r.text)
			self.status = 'Too many requests'
		elif r.status_code[0] == 5:
			self.status = 'Server error'
		else:
			self.status = 'Error tokenizing'

		self.update_status.emit(self.status)
		print(self.status)
		return False