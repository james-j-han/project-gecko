from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtNetwork

from bs4 import BeautifulSoup

import requests
import json
import time

import gecko_utils
from walmart_encryption import walmart_encryption

# VERSION 0.1
class Walmart(QObject):

	update_status = pyqtSignal(str)
	update_title = pyqtSignal(str)
	update_image = pyqtSignal(str)
	
	request_captcha = pyqtSignal()
	poll_response = pyqtSignal()
 
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,en;q=0.5',
		'Host': 'www.walmart.com',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
	}
	
	def __init__(self, search, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.proxy = None
		self.search = search
		self.profile = profile
		self.billing = billing

        # Webhook info
		self.store = 'https://www.walmart.com/'
		self.title = None
		self.src = None
		self.link = self.search
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		# Product info
		self.offer_ID = None
		self.item_ID = None
		self.ff_option = None
		self.ship_method = None
		self.PIE_L = None
		self.PIE_E = None
		self.PIE_K = None
		self.PIE_key_ID = None
		self.PIE_phase = None
		self.encrypted_card = None
		self.pi_hash = None
		self.payment_type = None

		# Other info
		self.status = 'Ready'
		self.current_step = 0
		self.steps = [
			self.search_for_product,
			self.add_to_cart,
			self.start_checkout,
			self.submit_shipping_method,
			self.submit_shipping,
			self.get_pie,
			self.submit_payment,
			self.submit_billing,
			self.submit_order,
			self.submit_webhook
		]

	def search_for_product(self):
		self.current_step = 0
		self.status = 'Searching for product'
		self.update_status.emit(self.status)
		print(self.status)
		try:
			r = self.s.get(self.search, headers=self.headers, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'lxml')
			item = soup.find('script', {'id': 'item'}).contents[0]
			data = json.loads(item)
			self.offer_ID = data['item']['product']['buyBox']['products'][0]['offerId']
			print(f'OFFER ID: {self.offer_ID}')
			self.title = data['item']['product']['buyBox']['products'][0]['productName']
			self.update_title.emit(self.title)
			self.src = data['item']['product']['buyBox']['products'][0]['images'][0]['url']
			# self.update_image.emit(self.src)
			return  True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def add_to_cart(self):
		self.current_step = 1
		self.status = 'Adding to cart'
		self.update_status.emit(self.status)
		print(self.status)
		h = self.headers
		h['Accept'] = 'application/json'
		h['Content-Type'] = 'application/json'
		url = 'https://www.walmart.com/api/v3/cart/guest/:CID/items'
		payload = {
			'location': {
				'city': self.profile.shipping_city,
				'isZipLocated': True,
				'postalCode': self.profile.shipping_zip,
				'state': self.profile.shipping_state
			},
			'offerId': self.offer_ID,
			'quantity': self.qty,
			'shipMethodDefaultRule': 'SHIP_RULE_1'
		}

		try:
			r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 201:
			data = r.json()
			# print(data)
			if data['checkoutable']:
				return True
		else:
			print(r.text)
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def start_checkout(self):
		self.current_step = 2
		self.status = 'Starting checkout'
		self.update_status.emit(self.status)
		print(self.status)
		h = self.headers
		h['Accept'] = 'application/json, text/javascript, */*; q=0.01'
		h['Referer'] = 'https://www.walmart.com/checkout/'
		h['WM_VERTICAL_ID'] = '0'
		url = 'https://www.walmart.com/api/checkout/v3/contract?page=CHECKOUT_VIEW'
		payload = {
			'affiliateInfo:com.wm.reflector': '',
			'city': self.profile.shipping_city,
			'crt:CRT': '',
			'customerId:CID': '',
			'customerType:type': '',
			'isZipLocated': True,
			'postalCode': self.profile.shipping_zip,
			'state': self.profile.shipping_state
		}

		try:
			r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 201:
			data = r.json()
			# print(data)
			self.item_ID = data['items'][0]['id']
			self.ff_option = data['items'][0]['fulfillmentSelection']['fulfillmentOption']
			self.ship_method = data['items'][0]['fulfillmentSelection']['shipMethod']
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)
			print(r.text)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_shipping_method(self):
		self.current_step = 3
		self.status = 'Submitting shipping method'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.walmart.com/api/checkout/v3/contract/:PCID/fulfillment'
		payload = {
			'groups': [{
				'fulfillmentOption': self.ff_option,
				'itemIds': [self.item_ID],
				'shipMethod': self.ship_method
			}]
		}

		try:
			r = self.s.post(url, headers=self.headers, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_shipping(self):
		self.current_step = 4
		self.status = 'Submitting shipping'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.walmart.com/api/checkout/v3/contract/:PCID/shipping-address'
		payload = {
			'addressLineOne': self.profile.shipping_address,
			'addressLineTwo': self.profile.shipping_address_2,
			'addressType': 'RESIDENTIAL',
			'changedFields': [],
			'city': self.profile.shipping_city,
			'countryCode': 'USA',
			'email': self.profile.email,
			'firstName': self.profile.first_name,
			'lastName': self.profile.last_name,
			'marketingEmailPref': False,
			'phone': self.profile.phone,
			'postalCode': self.profile.shipping_zip,
			'state': self.profile.shipping_state
		}

		try:
			r = self.s.post(url, headers=self.headers, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def get_pie(self):
		self.current_step = 5
		self.status = 'Getting PIE'
		self.update_status.emit(self.status)
		print(self.status)
		h = self.headers
		h['Accept'] = '*/*'
		h['Host'] = 'securedataweb.walmart.com'
		url = 'https://securedataweb.walmart.com/pie/v1/wmcom_us_vtg_pie/getkey.js'
		params = {
			'bust': int(time.time())
		}

		try:
			r = self.s.get(url, headers=h, params=params, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			pie = r.text
			self.PIE_L = int(pie.split('PIE.L = ')[1].split(';')[0])
			self.PIE_E = int(pie.split('PIE.E = ')[1].split(';')[0])
			self.PIE_K = pie.split('PIE.K = "')[1].split('";')[0]
			self.PIE_key_ID = pie.split('PIE.key_id = "')[1].split('";')[0]
			self.PIE_phase = int(pie.split('PIE.phase = ')[1].split(';')[0])
			self.encrypted_card = walmart_encryption.encrypt(self.billing.card_number, self.billing.cvv, self.PIE_L, self.PIE_E, self.PIE_K, self.PIE_key_ID, self.PIE_phase)
			print(self.encrypted_card[0])
			print(self.encrypted_card[1])
			print(self.encrypted_card[2])
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_payment(self):
		self.current_step = 6
		self.status = 'Submitting payment'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.walmart.com/api/checkout-customer/:CID/credit-card'
		h = self.headers
		h['Accept'] = 'application/json'
		h['Content-Type'] = 'application/json'
		payload = {
			'addressLineOne': self.profile.billing_address,
			'addressLineTwo': self.profile.billing_address_2,
			'addressType': 'RESIDENTIAL',
			'cardType': self.billing.card_type.upper(),
			'city': self.profile.billing_city,
			'encryptedCvv': self.encrypted_card[1],
			'encryptedPan': self.encrypted_card[0],
			'expiryMonth': self.billing.exp_month,
			'expiryYear': self.billing.exp_year,
			'firstName': self.profile.first_name,
			'integrityCheck': self.encrypted_card[2],
			'isGuest': True,
			'keyId': self.PIE_key_ID,
			'lastName': self.profile.last_name,
			'phase': self.PIE_phase,
			'phone': self.profile.phone,
			'postalCode': self.profile.billing_zip,
			'state': self.profile.billing_state
		}

		try:
			r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			self.pi_hash = data['piHash']
			self.payment_type = data['paymentType']
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_billing(self):
		self.current_step = 7
		self.status = 'Submitting billing'
		self.update_status.emit(self.status)
		print(self.status)
		h = self.headers
		h['Accept'] = 'application/json, text/javascript, */*; q=0.01'
		h['Content-Type'] = 'application/json'
		h['WM_VERTICAL_ID'] = '0'
		url = 'https://www.walmart.com/api/checkout/v3/contract/:PCID/payment'
		payload = {
			'payments': [{
				'addressLineOne': self.profile.billing_address,
				'addressLineTwo': self.profile.billing_address_2,
				'cardType': self.billing.card_type.upper(),
				'city': self.profile.billing_city,
				'email': self.profile.email,
				'encryptedCvv': self.encrypted_card[1],
				'encryptedPan': self.encrypted_card[0],
				'expiryMonth': self.billing.exp_month,
				'expiryYear': self.billing.exp_year,
				'firstName': self.profile.first_name,
				'integrityCheck': self.encrypted_card[2],
				'keyId': self.PIE_key_ID,
				'lastName': self.profile.last_name,
				'paymentType': self.payment_type,
				'phase': self.PIE_phase,
				'phone': self.profile.phone,
				'piHash': self.pi_hash,
				'postalCode': self.profile.billing_zip,
				'state': self.profile.billing_state
			}]
		}

		try:
			r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_order(self):
		self.current_step = 8
		self.status = 'Submitting order'
		self.update_status.emit(self.status)
		print(self.status)
		h = self.headers
		h['Accept'] = 'application/json, text/javascript, */*; q=0.01'
		h['Content-Type'] = 'application/json'
		h['WM_VERTICAL_ID'] = '0'
		url = 'https://www.walmart.com/api/checkout/v3/contract/:PCID/order'
		payload = {}

		try:
			r = self.s.put(url, headers=h, json=payload, proxies=self.proxy)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			self.order_number = data['order']['orderId']
			return True
		else:
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_webhook(self):
		self.current_step = 9
		self.status = f'Check email! Order #: {self.order_number}'
		self.update_status.emit(self.status)
		print(self.status)
		try:
			gecko_utils.post_webhook(self.title, self.store, self.link, self.price, self.qty, self.src, self.color, self.size)
		except Exception as e:
			print(f'{e}')
		
		return True