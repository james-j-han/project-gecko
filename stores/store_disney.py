from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtNetwork

from bs4 import BeautifulSoup

import requests
import json
import time

class Disney(QObject):

	update_status = pyqtSignal(str)
	update_title = pyqtSignal(str)
	update_image = pyqtSignal(str)
	
	request_captcha = pyqtSignal()
	poll_response = pyqtSignal()
 
	headers = {
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'host': 'www.shopdisney.com',
		'origin': 'https://www.shopdisney.com',
		'pragma': 'no-cache',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
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
		self.store = 'https://www.shopdisney.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		self.pid = '427245425113'
		self.qty = '1'
		self.category = 'accessories-women-jewelry+%26+watches'

		self.abort = False
		self.shipmentUUID = None
		self.csrf_token = None
		self.shipping_ID = None
		self.captcha_url = 'https://www.shopdisney.com/checkout?stage=payment#payment'
		self.waiting_for_captcha = False
		self.g_recaptcha_response = None
		self.cookies = []
		self.access_token = None
		self.address_ID = None

		self.status = 'Ready'

		self.steps = [
			self.add_to_cart,
			self.start_checkout,
			self.submit_shipping,
			self.captcha,
			self.google_recaptcha,
			self.validate_basket,
			self.auth_token,
			self.submit_billing
		]

	def add_to_cart(self):
		self.status = 'Adding to cart'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Cart-AddProduct'
		payload = {
			'pid': self.pid,
			'quantity': self.qty,
			'productGuestCategory': self.category
		}
		r = self.s.post(url, headers=self.headers, data=payload)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
			print(f'shipmentUUID: {self.shipmentUUID}')
			self.shipping_ID = data['cart']['shipments'][0]['selectedShippingMethod']
			print(f'Shipping ID: {self.shipping_ID}')
			return True
		else:
			print(r.text)

		self.staus = 'Error carting'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def start_checkout(self):
		self.status = 'Starting checkout'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.shopdisney.com/checkout'
		r = self.s.get(url, headers=self.headers)
		print(r)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'lxml')
			self.csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
			print(f'CSRF TOKEN: {self.csrf_token}')
			return True
		else:
			pass

		self.status = 'Error starting checkout'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_shipping(self):
		self.status = 'Submitting shipping'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/CheckoutShippingServices-SubmitShipping'
		payload = {
			'originalShipmentUUID': self.shipmentUUID,
			'shipmentUUID': self.shipmentUUID,
			'dwfrm_shipping_shippingAddress_addressFields_country': 'US',
			'dwfrm_shipping_shippingAddress_addressFields_firstName': 'James',
			'dwfrm_shipping_shippingAddress_addressFields_lastName': 'Doe',
			'dwfrm_shipping_shippingAddress_addressFields_address1': '2863 Forest Chase Dr NE',
			'dwfrm_shipping_shippingAddress_addressFields_address2': '',
			'dwfrm_shipping_shippingAddress_addressFields_postalCode': '30066',
			'dwfrm_shipping_shippingAddress_addressFields_city': 'Marietta',
			'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': 'GA',
			'dwfrm_shipping_shippingAddress_addressFields_phone': '+17737081444',
			'shippingMethod': self.shipping_ID,
			'csrf_token': self.csrf_token
		}
		r = self.s.post(url, headers=self.headers, data=payload)
		print(r)
		if r.status_code == 200:
			# data = r.json()
			# self.captcha_url = r.url
			# print(self.captcha_url)
			return True
		else:
			print(r.text)

		self.status = 'Error submitting shipping'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def captcha(self):
		self.status = 'Waiting for captcha'
		self.update_status.emit(self.status)
		print(self.status)
		# Save cookies and send with along with emit signal
		self.cookies = []
		for cookie in self.s.cookies:
			c = QtNetwork.QNetworkCookie()
			c.setDomain(cookie.__dict__['domain'])
			c.setName(bytes(cookie.__dict__['name'], 'utf-8'))
			c.setValue(bytes(cookie.__dict__['value'], 'utf-8'))
			self.cookies.append(c)
		# Emit signal to load captcha and browser
		self.request_captcha.emit()
		# self.waiting_for_captcha = True
		# while self.waiting_for_captcha:
		while True:
			if self.abort:
				return False
			else:
				if self.g_recaptcha_response is None:
					print('Waiting for captcha')
					self.poll_response.emit()
					time.sleep(1)
				else:
					return True

	def google_recaptcha(self):
		self.status = 'Google recaptcha'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Google-reCaptcha'
		payload = {
			'dwfrm_billing_addressFields_firstName': 'James',
			'dwfrm_billing_addressFields_lastName': 'Doe',
			'dwfrm_billing_addressFields_address1': '2863 Forest Chase Dr NE',
			'dwfrm_billing_addressFields_address2': '',
			'dwfrm_billing_addressFields_country': 'US',
			'dwfrm_billing_addressFields_states_stateCode': 'GA',
			'dwfrm_billing_addressFields_city': 'Marietta',
			'dwfrm_billing_addressFields_postalCode': '30066',
			'dwfrm_billing_paymentDetails': '',
			'dwfrm_billing_commerceId': '',
			'dwfrm_billing_vcoWalletRefId': '',
			'dwfrm_billing_creditCardFields_email': 'semajhan@gmail.com',
			'g-recaptcha-response': self.g_recaptcha_response
		}
		h = self.headers
		h['content-type'] = 'application/x-www-form-urlencoded'
		r = self.s.post(url, headers=h, data=payload)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True

		self.status = 'Error google recaptcha'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def validate_basket(self):
		self.status = 'Validating basket'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Checkout-ValidateBasket'
		payload = {
			'dwfrm_billing_addressFields_firstName': 'James',
			'dwfrm_billing_addressFields_lastName': 'Doe',
			'dwfrm_billing_addressFields_address1': '2863 Forest Chase Dr NE',
			'dwfrm_billing_addressFields_address2': '',
			'dwfrm_billing_addressFields_country': 'US',
			'dwfrm_billing_addressFields_states_stateCode': 'GA',
			'dwfrm_billing_addressFields_city': 'Marietta',
			'dwfrm_billing_addressFields_postalCode': '30066',
			'dwfrm_billing_paymentDetails': '',
			'dwfrm_billing_commerceId': '',
			'dwfrm_billing_vcoWalletRefId': '',
			'dwfrm_billing_creditCardFields_email': 'semajhan@gmail.com',
			'g-recaptcha-response': self.g_recaptcha_response
		}
		h = self.headers
		h['referer'] = 'https://www.shopdisney.com/checkout?stage=payment'
		r = self.s.post(url, headers=h, data=payload)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True

		self.status = 'Error validating basket'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def auth_token(self):
		self.status = 'Auth token'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://authorization.go.com/token'
		payload = {
			'client_id': 'DSI-DISHOPWEB-PROD',
			'grant_type': 'assertion',
			'assertion_type': 'public'
		}
		r = self.s.post(url, headers=self.headers, data=payload)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.access_token = data['access_token']
			print(f'ACCESS TOKEN: {self.access_token}')
			return True

		self.status = 'Error auth token'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def submit_billing(self):
		self.status = 'Submitting billing'
		self.update_status.emit(self.status)
		print(self.status)				
		url = 'https://www.shopdisney.com/api/addresses'
		h = self.headers
		h['content-type'] = 'application/json'
		h['Authorization'] = f'BEARER {self.access_token}'
		payload = {
			'addresses': [
				{
					'address1': '2863 Forest Chase Dr NE',
					'address2': '',
					'city': 'Marietta',
					'country': 'US',
					'first_name': 'James',
					'last_name': 'Doe',
					'phone1': '+17737081444',
					'state': 'GA',
					'type': 'SB',
					'zip_code': '30066'
				}
			]
		}
		r = self.s.post(url, headers=h, json=payload)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.address_ID = data['addresses'][0]['address_id']
			return False
		elif r.status_code == 401:
			self.status = 'Unauthorized'
			self.update_status.emit(self.status)
			print(self.status)
			print(r.text)
			return False
		else:
			print(r.text)

		self.status = 'Error submitting billing'
		self.update_status.emit(self.status)
		print(self.status)
		return False