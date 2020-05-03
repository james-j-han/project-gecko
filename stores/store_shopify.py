from PyQt5.QtCore import QObject, pyqtSignal, QByteArray
from PyQt5 import QtCore, QtNetwork
from bs4 import BeautifulSoup

import gecko_utils

import requests
import json
import time
import uuid

class Shopify(QObject):

	update_product_image = pyqtSignal(str)
	update_product_title = pyqtSignal(str)
	update_product_size = pyqtSignal(str)
	
	update_task_status = pyqtSignal(str)
	update_task_log = pyqtSignal(str)
	request_render = pyqtSignal(str, list)

	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
	}

	def __init__(self, base_url, api_key, keywords, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.abort = False
		self.release = '2020-01'

		self.base_url = base_url
		self.api_key = api_key
		self.keywords = keywords
		self.qty = qty
		self.size = size
		self.color = color
		self.profile = profile
		self.billing = billing

		self.token = None
		self.cookies = []
		self.rendered_html = None
		self.rendering = True
		self.payment_due = None

		self.resolution = gecko_utils.get_random_client_resolution()

		# self.url_products = f'{self.base_url}products.json'

		self.status = {
			'captcha_detected': False,
			'search_all_products': False,
			'add_to_cart': False,
			'start_checkout': False,
			'submit_info': False,
			'submit_shipping': False,
			'submit_payment': False,
			'checkout_successful': False
		}

	# Get all products
	def search_all_products(self, proxy=None):
		print('Searching for product')
		limit = 250
		page = 1
		while True:
			if self.abort:
				return False
			else:
				url = f'{self.base_url}products.json?limit={limit}&page={page}'
				# url = '{}?limit={}&page={}'.format(self.url_products, limit, page)
				try:
					r = self.s.get(url, headers=self.headers, proxies=proxy)
					data = json.loads(r.text)
					product_count = len(data['products'])
					if product_count > 0:
						for p in data['products']:
							if self.abort:
								return False
							else:
								if self.search_for_product(p): return True
						if product_count < limit:
							return False
					else:
						return False
					page += 1
				except requests.exceptions.ProxyError as e:
					print('[EXCEPTION] {}'.format(e))
					self.update_task_status.emit('Proxy error')
					return False
				except Exception as e:
					print('[EXCEPTION] {}'.format(e))
					return False

	# Search for matching product
	def search_for_product(self, product):
		title = product['title']
		image_url = product['images'][0]['src']
		if all(kw in title.lower() for kw in self.keywords['pos']):
			if self.keywords['neg']:
				if any(kw in title.lower() for kw in self.keywords['neg']):
					return False

			self.title = title
			self.src = image_url
			self.update_product_title.emit(self.title)
			self.update_product_image.emit(self.src)
			if self.search_for_size(product['variants']):
				self.update_product_size.emit(self.size_emit)
				# self.update_status(self.title, self.src, self.size_emit)
				self.direct_link = f'{self.base_url}products/{product["handle"]}'
				# self.direct_link = '{}{}'.format(self.url_product, product['handle'])
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
			self.size_emit = variants[random_size]['title']
			return True
		else:
			for variant in variants:
				if self.size.lower() in variant['title'].lower():
					self.variant_id = variant['id']
					self.size_emit = variant['title']
					return True
		return False

	def update_status(self, title, src, size):
		self.update_product_title.emit(title)
		self.update_product_image.emit(src)
		self.update_product_size.emit(size)

	def add_to_cart(self, proxy=None):
		print('Adding to cart')
		api_headers = self.headers
		api_headers['x-shopify-storefront-access-token'] = self.api_key
		api_headers['content-type'] = 'application/json'
		url = f'{self.base_url}api/{self.release}/checkouts.json'
		payload = {
			'checkout': {
				'line_items': [{
					'variant_id': self.variant_id,
					'quantity': self.qty
				}],
				'email': self.profile.email,
				'phone': self.profile.phone,
				'shipping_address': {
					'first_name': self.profile.first_name,
					'last_name': self.profile.last_name,
					'address1': self.profile.shipping_address,
					'address2': self.profile.shipping_address_2,
					'city': self.profile.shipping_city,
					'country': 'US',
					'province': self.profile.shipping_state,
					'phone': self.profile.phone,
					'zip': self.profile.shipping_zip
				},
				'billing_address': {
					'first_name': self.profile.first_name,
					'last_name': self.profile.last_name,
					'address1': self.profile.shipping_address,
					'address2': self.profile.shipping_address_2,
					'city': self.profile.shipping_city,
					'country': 'US',
					'province': self.profile.shipping_state,
					'phone': self.profile.phone,
					'zip': self.profile.shipping_zip
				}
			}
		}
		r = self.s.post(url, headers=api_headers, json=payload, proxies=proxy).json()
		try:
			self.token = r['checkout']['token']
			self.vault_url = r['checkout']['payment_url']
			self.checkout_url = r['checkout']['web_url']
			return True
		except:
			return False

	def start_checkout(self, proxy=None):
		print('Starting checkout')
		r = self.s.get(self.checkout_url, headers=self.headers, proxies=proxy)
		soup = BeautifulSoup(r.text, 'html.parser')
		self.auth_token = soup.find('input', {'name': 'authenticity_token'})['value']
		if gecko_utils.detect_captcha(r.text):
			self.status['captcha_detected'] = True
		return True

	def submit_info(self, proxy=None):
		print('Submitting info')
		payload = {
			'_method': 'patch',
			'authenticity_token': self.auth_token,
			'previous_step': 'contact_information',
			'step': 'shipping_method',
			'g-recaptcha-response': self.token
		}
		post_headers = self.headers
		post_headers['content-type'] = 'application/x-www-form-urlencoded'
		r = self.s.post(self.checkout_url, headers=post_headers, data=payload, proxies=proxy)
		soup = BeautifulSoup(r.text, 'html.parser')
		title = soup.find('title')
		if not 'error' in str(title):
			return True
		else:
			return False
		# self.token = 'f551f223a101f58c7da26f58fc6ab856'
		# api_headers = self.headers
		# api_headers['x-shopify-storefront-access-token'] = self.api_key
		# api_headers['content-type'] = 'application/json'
		# url = f'{self.base_url}api/{self.release}/checkouts/{self.token}.json'
		# payload = {
		# 	'checkout': {
		# 		'token': self.token,
		# 		'shipping_address': {
		# 			'first_name': self.profile.first_name,
		# 			'last_name': self.profile.last_name,
		# 			'address1': self.profile.shipping_address,
		# 			'address2': self.profile.shipping_address_2,
		# 			'city': self.profile.shipping_city,
		# 			'country': 'US',
		# 			'province': self.profile.shipping_state,
		# 			'phone': self.profile.phone,
		# 			'zip': self.profile.shipping_zip
		# 		},
		# 		'billing_address': {
		# 			'first_name': self.profile.first_name,
		# 			'last_name': self.profile.last_name,
		# 			'address1': self.profile.shipping_address,
		# 			'address2': self.profile.shipping_address_2,
		# 			'city': self.profile.shipping_city,
		# 			'country': 'US',
		# 			'province': self.profile.shipping_state,
		# 			'phone': self.profile.phone,
		# 			'zip': self.profile.shipping_zip
		# 		}
		# 	}
		# }
		# r = self.s.put(url, headers=api_headers, json=payload, proxies=proxy).json()
		# print(r)
		# return True

	def submit_shipping(self, proxy=None):
		print('Submitting shipping')
		self.token = '7759338542b94a6d827badd9ec5849f4'
		api_headers = self.headers
		api_headers['x-shopify-storefront-access-token'] = self.api_key
		api_headers['content-type'] = 'application/json'
		url = f'{self.base_url}api/{self.release}/checkouts/{self.token}/shipping_rates.json'
		r = self.s.get(url, headers=api_headers, proxies=proxy).json()
		try:
			self.shipping_handle = r['shipping_rates'][0]['id']
		except:
			return False

		url = f'{self.base_url}api/{self.release}/checkouts/{self.token}.json'
		payload = {
			'checkout': {
				'token': self.token,
				'shipping_line': {
					'handle': self.shipping_handle
				}
			}
		}
		r = self.s.put(url, headers=api_headers, json=payload, proxies=proxy).json()
		try:
			shipping_rate = r['checkout']['shipping_rate']
			self.payment_due = r['checkout']['payment_due']
			print(type(self.payment_due))
			self.checkout_url = r['checkout']['web_url']
			self.vault_url = r['checkout']['payment_url']
			print(self.payment_due)
			return True
		except:
			return False

	def submit_payment(self, proxy=None):
		print('Submitting payment')
		self.cookies = []
		for cookie in self.s.cookies:
			c = QtNetwork.QNetworkCookie()
			c.setDomain(cookie.__dict__['domain'])
			c.setName(bytes(cookie.__dict__['name'], 'utf-8'))
			c.setValue(bytes(cookie.__dict__['value'], 'utf-8'))
			self.cookies.append(c)
		self.request_render.emit(self.checkout_url, self.cookies)
		self.rendering = True
		while self.rendering:
			time.sleep(0.1)
		soup = BeautifulSoup(self.rendered_html, 'html.parser')
		# with open('test_funkoshop.html', mode='w', encoding='utf-8') as f:
		# 	f.write(soup.prettify())
		tokens = soup.find_all('input', {'name': 'authenticity_token'})
		print(len(tokens))
		auth_token = tokens[2]['value']
		print(auth_token)
		gateway = soup.find('input', {'name': 'checkout[payment_gateway]'})['value']
		print(gateway)
		payload = {
			'credit_card': {
				'number': f'{self.billing.card_number[:4]} {self.billing.card_number[4:8]} {self.billing.card_number[8:12]} {self.billing.card_number[12:]}',
				'name': self.billing.name_on_card,
				'month': self.billing.exp_month,
				'year': self.billing.exp_year,
				'verification_value': self.billing.cvv
			}
		}
		print(payload)
		r = self.s.post(self.vault_url, headers=self.headers, json=payload, proxies=proxy).json()
		try:
			session_id = r['id']
			print(session_id)
		except:
			return False

		payload = {
			'_method': 'patch',
			'authenticity_token': auth_token,
			'previous_step': 'payment_method',
			'step': '',
			's': session_id,
			'checkout[payment_gateway}': gateway,
			'checkout[credit_card][vault]': 'false',
			'checkout[different_billing_address]': 'false',
			'checkout[total_price]': self.payment_due.replace('.', ''),
			'complete': '1',
			'checkout[client_details][browser_width]': self.resolution['width'],
			'checkout[client_details][browser_height]': self.resolution['height'],
			'checkout[client_details][javascript_enabled]': '1',
			'checkout[client_details][color_depth]': '24',
			'checkout[client_details][java_enabled]': 'false',
			'checkout[client_details][browser_tz]': '240'
		}

		post_headers = self.headers
		post_headers['content-type'] = 'application/x-www-form-urlencoded'

		r = self.s.post(self.checkout_url, headers=post_headers, data=payload, proxies=proxy)
		return True
		
	def verify_checkout(self, proxy=None):
		host = self.base_url.split('/')[-2]
		api_headers = self.headers
		api_headers['host'] = host
		api_headers['x-shopify-storefront-access-token'] = self.api_key
		api_headers['content-type'] = 'application/json'
		url = f'{self.base_url}api/{self.release}/checkouts/{self.token}.json'
		r = self.s.get(url, headers=api_headers, proxies=proxy).json()
		print(r)
		if r['checkout']['payments']:
			status = r['checkout']['payments'][-1]['transaction']['status']
			print(status)
			if 'fail' in status.lower():
				return False
			else:
				return True
		else:
			return False