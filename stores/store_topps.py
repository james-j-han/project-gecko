from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtNetwork

from bs4 import BeautifulSoup

import requests
import json
import time

import gecko_utils

# VERSION 1.2
class Topps(QObject):

	update_title = pyqtSignal()
	update_image = pyqtSignal()
	update_size = pyqtSignal()
	update_status = pyqtSignal()
	
	request_captcha = pyqtSignal()
	poll_response = pyqtSignal()
 
	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		'host': 'www.topps.com',
		'pragma': 'no-cache',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
	}
	
	def __init__(self, task_type, search, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.task_type = task_type
		self.search = search
		self.profile = profile
		self.billing = billing

        # Webhook info
		self.store = 'https://www.shopdisney.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		# Product info
		self.pid = search.split('-')[-1].split('.')[0]
		self.abort = False
		self.shipmentUUID = None
		self.csrf_token = None
		self.shipping_ID = None
		self.captcha_url = 'https://www.shopdisney.com/checkout?stage=payment#payment'
		self.waiting_for_captcha = False
		self.g_recaptcha_response = None
		self.cookies = []
		self.bearer = None
		self.access_token = None
		self.address_ID = None
		self.order_number = None
		self.commerce_ID = None
		self.payment_ID = None
		self.total_price = None
		self.conversation_ID = None

		# Other info
		self.status = 'Ready'
		self.current_step = 0
		if self.task_type == 'Normal':
			self.steps = [
				self.check_queue,
				self.add_to_cart,
				self.validate_basket,
				self.validate_checkout,
				self.start_checkout,
				self.submit_shipping,
				self.captcha,
				self.google_recaptcha,
				self.checkout_validate_basket,
				self.auth_token,
				self.submit_billing,
				self.submit_order,
				self.submit_payment,
				self.get_order,
				self.verify_order,
				self.checkout_submit_order,
				# self.order_confirmation,
				self.submit_webhook
			]

		self.in_stock = False
		if self.task_type == 'Monitor':
			self.steps = [
				self.monitor,
				self.submit_webhook_2
			]

	def check_queue(self):
		self.current_step = 0
		self.status = 'Checking queue'
		self.update_status.emit()
		print(self.status)

		try:
			r = self.s.get(self.search, headers=self.headers)
		except Exception as e:
			print(f'{e}')

		print(r)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'lxml')
			title = soup.find('h1', {'id': 'heading'})
			if title:
				if 'waiting' in title.text.lower():
					self.status = 'Waiting in queue'
			else:
				return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit()
		print(self.status)
		return False

	def add_to_cart(self):
		self.current_step = 1
		self.status = 'Adding to cart'
		self.update_status.emit()
		print(self.status)
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Cart-AddProduct'
		payload = {
			'pid': self.pid,
			'quantity': self.qty
			# 'productGuestCategory': self.category
		}
		try:
			r = self.s.post(url, headers=self.headers, data=payload)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			# print(data)
			try:
				if data['quantityTotal'] > 0:
					self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
					self.shipping_ID = data['cart']['shipments'][0]['selectedShippingMethod']
					self.title = data['cart']['items'][0]['productName']
					self.update_title.emit()
					self.price = data['cart']['items'][0]['price']['sales']['formatted']
					src = data['cart']['items'][0]['images']['small'][0]['url']
					self.src = f'http://{src.split("//")[-1]}'
					self.update_image.emit()
					self.link = f'https://www.shopdisney.com/{self.pid}.html'
					# self.link = self.s.get(url, headers=self.headers).url
					self.update_size.emit()
					return True
				if data['isSoldOut']:
					self.status = 'Out of stock'
			except Exception as e:
				print(f'{e}')
		else:
			# print(r.text)
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit()
		print(self.status)
		return False

	def submit_webhook(self):
		self.current_step = 16
		self.status = f'Check email! Order #: {self.order_number}'
		self.update_status.emit()
		print(self.status)
		try:
			gecko_utils.post_webhook(self.title, self.store, self.link, self.price, self.qty, self.src, self.color, self.size)
		except Exception as e:
			print(f'{e}')

		return True