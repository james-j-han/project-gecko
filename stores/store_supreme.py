from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtNetwork
from bs4 import BeautifulSoup
from webhook import Webhook
from webpage import Webpage

import requests
import random
import json
import time
import urllib.parse
import threading

class Supreme(QObject):

	update_product_image = pyqtSignal(str)
	update_product_title = pyqtSignal(str)
	update_product_size = pyqtSignal(str)
	update_task_status = pyqtSignal(str)
	update_task_log = pyqtSignal(str)

	request_render = pyqtSignal()
	captcha_detected = pyqtSignal()
	request_poll_token = pyqtSignal()

	store = 'https://www.supremenewyork.com/'
	url_products = 'https://www.supremenewyork.com/mobile_stock.json'
	url_product = None
	url_styles_js = 'https://www.supremenewyork.com/shop/' # <id>.json
	url_add_js = 'https://www.supremenewyork.com/shop/' # <id>/add.json
	url_cart_js = 'https://www.supremenewyork.com/shop/cart.json'
	url_checkout = 'https://www.supremenewyork.com/checkout.json'
	url_status = 'https://www.supremenewyork.com/checkout/' # <slug>/status.json

	headers = {
		'authority': 'www.supremenewyork.com',
		'accept': 'text/html, application/xhtml+xml, application/xml',
		'accept-encoding': 'gzip, deflate, br',
		'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/76.0.3809.132 Mobile/13B143 Safari/601.1.46'
	}

	lock = threading.Lock()

	def __init__(self, s, task_type, captcha_logic, keywords, qty, category, size, color, profile, billing):
		QObject.__init__(self)

		self.title = None
		self.src = None
		self.style_id = None
		self.variant_id = None
		self.price = None
		self.direct_link = None
		self.authenticity_token = None
		self.shipping_code = None
		self.checkout_price = None
		self.sitekey = '6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz'

		self.s = s
		self.task_type = task_type
		self.captcha_logic = captcha_logic
		self.keywords = keywords
		self.qty = qty
		self.category = category
		self.size = size
		self.color = color
		self.profile = profile
		self.billing = billing
		self.token = None
		self.size_emit = None
		self.slug = None
		
		self.page = Webpage()
		self.cookies = []
		self.client_width = None
		self.client_height = None
		self.random_client_resolution()
		self.waiting_for_captcha = False
		self.abort = False

		self.status = {
			'search_all_products': False,
			'add_to_cart': False,
			'start_checkout': False,
			'submit_info': False,
			'submit_shipping': False,
			'submit_payment': False,
			'checkout_successful': False
		}

	def random_client_resolution(self):
		self.client_width = random.randint(800, 1921)
		self.client_height = random.randint(600, 1081)
		print('Client Window Resolution: {}x{}'.format(self.client_width, self.client_height))

	def render_page(self):
		self.page.set_cookies(self.cookies)
		self.page.loadFinished.connect(self.set_html)
		self.page.load(QtCore.QUrl(self.url_step))

	def set_html(self):
		self.page.page.toHtml(self.callable)

	def callable(self, data):
		self.page.html = data

	def rendering_page(self):
		while self.page.html is None:
			if self.abort:
				self.page.stop()
				return False
			else:
				time.sleep(0.1)
		return True

	def detect_captcha(self, soup=None):
		if soup is None:
			self.captcha_detected.emit()
			self.waiting_for_captcha = True
			while self.waiting_for_captcha:
				if self.abort:
					break
				else:
					print('Polling for token')
					self.request_poll_token.emit()
					time.sleep(0.5)
		else:
			if self.captcha_logic == QtCore.Qt.Unchecked:
				print('Ignoring captcha')
			elif self.captcha_logic == QtCore.Qt.PartiallyChecked or self.captcha_logic == QtCore.Qt.Checked:
				captcha = soup.find('textarea', id='g-recaptcha-response')
				if captcha:
					self.captcha_detected.emit()
					self.waiting_for_captcha = True
					while self.waiting_for_captcha:
						print('Polling for token')
						self.request_poll_token.emit()
						time.sleep(0.5)
				else:
					print("No captcha detected")
			else:
				print('Error with logic')

	# Get all products
	def search_all_products(self, proxy=None):
		# print('Searching for product')
		while True:
			if self.abort:
				return False
			else:
				try:
					r = self.s.get(self.url_products, headers=self.headers, proxies=proxy)
					# cache = r.headers['x-cache']
					# print('cache: {}'.format(cache))
					data = r.json()
					# print(data)

					for category in data['products_and_categories']:
						if self.abort:
							return False
						else:
							if self.category.lower() == category.lower():
								for p in data['products_and_categories']['{}'.format(self.category)]:
									if self.search_for_product(p, proxy): return True
					return False
				except requests.exceptions.ProxyError as e:
					print('[EXCEPTION] {}'.format(e))
					self.update_task_status.emit('Proxy error')
					return False
				except Exception as e:
					print('[EXCEPTION] {}'.format(e))
					return False

	# Search for matching product
	def search_for_product(self, product, proxy):
		title = product['name']
		if all(kw in title.lower() for kw in self.keywords['pos']):
			if self.keywords['neg']:
				if any(kw in title.lower() for kw in self.keywords['neg']):
					return False

			self.title = title
			self.update_product_title.emit(self.title)
			product_id = product['id']
			url = '{}{}.json'.format(self.url_styles_js, product_id)
			r = self.s.get(url, headers=self.headers, proxies=proxy)
			data = r.json()

			for style in data['styles']:
				title = style['name']
				if self.color.lower() == title.lower():
					self.style_id = style['id']
					self.src = 'http:{}'.format(style['image_url_hi'])
					self.update_product_image.emit(self.src)

					if self.search_for_size(style['sizes']):
						self.update_product_size.emit(self.size_emit)
						return True
					else:
						self.update_task_status.emit('Size unavailable')
						return False
		else:
			return False

	# Search for size/variant
	def search_for_size(self, variants):
		if self.size == 'N/A':
			self.variant_id = variants[0]['id']
			self.size_emit = self.size
			return True
		elif self.size == 'Any':
			variant_count = len(variants)
			random_size = random.randint(0, variant_count)
			self.variant_id = variants[random_size]['id']
			self.size_emit = variants[random_size]['name']
			return True
		else:
			for variant in variants:
				if self.size.lower() in variant['name'].lower():
					self.variant_id = variant['id']
					self.size_emit = variant['name']
					return True
		return False

	def add_to_cart(self, proxy=None):
		payload = {
			's': self.variant_id,
			'st': self.style_id,
			'qty': self.qty
		}

		post_headers = self.headers
		post_headers['content-type'] = 'application/x-www-form-urlencoded'

		url = '{}{}/add.json'.format(self.url_add_js, self.variant_id)
		r = self.s.post(url, headers=self.headers, data=payload, proxies=proxy)
		data = json.loads(r.text)
		print(data)

		if data:
			if data[0]['in_stock']:
				# Successful
				return True
			else:
				return False
		else:
			self.status['search_all_products'] = False
			return False

	def start_checkout(self, proxy=None):
		self.detect_captcha()
		return True

	def submit_info(self, proxy=None):
		return True

	def submit_shipping(self, proxy=None):
		return True

	def submit_payment(self, proxy=None):
		phone = '{}-{}-{}'.format(self.profile.phone[:3], self.profile.phone[3:6], self.profile.phone[6:])
		card = '{} {} {} {}'.format(self.billing.card_number[:4], self.billing.card_number[4:8], self.billing.card_number[8:12], self.billing.card_number[12:])
		decoded = '{{"{}":{}}}'.format(self.variant_id, self.qty)
		cookie_sub = urllib.parse.quote('{}'.format(decoded), safe='()')

		payload = {
			'store_credit_id': '',
			'from_mobile': '1',
			'cookie-sub': cookie_sub,
			'same_as_billing_address': '1',
			'scerkhaj': 'CKCRSUJHXH',
			'order[billing_name]': '',
			'order[bn]': '{} {}'.format(self.profile.first_name, self.profile.last_name),
			'order[email]': self.profile.email,
			'order[tel]': phone,
			'order[billing_address]': self.profile.billing_address,
			'order[billing_address_2]': self.profile.billing_address_2,
			'order[billing_zip]': self.profile.billing_zip,
			'order[billing_city]': self.profile.billing_city,
			'order[billing_state]': self.profile.billing_state,
			'order[billing_country]': 'USA',
			'riearmxa': card,
			'credit_card[month]': self.billing.exp_month,
			'credit_card[year]': self.billing.exp_year,
			'credit_card[meknk]': self.billing.cvv,
			'order[terms]': '0',
			'order[terms]': '1',
			'g-recaptcha-response': self.token,
			'is_from_android': '1'
		}

		post_headers = self.headers
		post_headers['content-type'] = 'application/x-www-form-urlencoded'
		post_headers['accept'] = 'application/json'

		r = self.s.post(self.url_checkout, headers=post_headers, data=payload, proxies=proxy)
		data = r.json()
		print(data)
		status = None
		try:
			status = data['status'].lower()
		except Exception as e:
			print(str(e))
		print('Status: {}'.format(status))

		if status == 'failed':
			for key in self.status.keys():
				self.status[key] = False
			return False
		elif status == 'outofstock':
			self.update_task_status.emit('Out of stock')
			return False
		else:
			if data['slug']:
				self.slug = data['slug']
				return True
			else:
				return False
		# return True

		# if status == 'queued':
		# 	self.slug = data['slug']
		# 	return True
		# else:
		# 	for key in self.status.keys():
		# 		self.status[key] = False
		# 	return False

	def verify_checkout(self, proxy=None):
		url = '{}{}/status.json'.format(self.url_status, self.slug)
		r = self.s.get(url, headers=self.headers, proxies=proxy)
		data = r.json()
		print(data)
		status = None
		try:
			status = data['status']
		except Exception as e:
			print(str(e))
		
		if status == 'queued':
			return False
		elif status == 'failed':
			for key in self.status.keys():
				self.status[key] = False
			return False
		else:
			try:
				webhook = Webhook(self.title, self.store, self.direct_link, self.price, self.qty, self.src, self.color, self.size)
			except Exception as e:
				print(str(e))
			finally:
				return True