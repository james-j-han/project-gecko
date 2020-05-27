from bs4 import BeautifulSoup

import requests
import json
import time

# VERSION 1.1
class Disney:
 
	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'accept-encoding': 'gzip, deflate, br',
		# 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'host': 'www.shopdisney.com',
		# 'origin': 'https://www.shopdisney.com',
		'pragma': 'no-cache',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
		'Upgrade-Insecure-Requests': '1',
		# 'x-requested-with': 'XMLHttpRequest'
	}
	
	def __init__(self):
		super().__init__()
		self.s = requests.Session()
		self.pid = '428405618185'
		# self.profile = profile
		# self.billing = billing

        # Webhook info
		self.store = 'https://www.shopdisney.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = 1
		# self.color = color
		# self.size = size

		# Product info
		self.abort = False
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

		# Other info
		# self.status = 'Ready'
		# self.current_step = 0
		# self.steps = [
		# 	self.add_to_cart,
		# 	self.validate_basket,
		# 	self.validate_checkout,
		# 	self.start_checkout,
		# 	self.submit_shipping,
		# 	self.captcha,
		# 	self.google_recaptcha,
		# 	self.checkout_validate_basket,
		# 	self.auth_token,
		# 	self.submit_billing,
		# 	self.submit_order,
		# 	self.submit_payment,
		# 	self.get_order,
		# 	self.verify_order,
		# 	self.checkout_submit_order,
		# 	self.order_confirmation,
		# 	self.submit_webhook
		# ]

	def handle_status(self, status_code):
		sc = int(str(status_code)[0])
		if sc == 4:
			if status_code == 429:
				self.status = 'Too many requests'
			else:
				self.status = 'Client error'
		elif sc == 5:
			self.status = 'Server error'
		else:
			self.status = 'Error'

	def get_page(self):
		print(f'''

============================================================
GETTING PAGE
============================================================

		''')
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/OneID-Responder'
		params = {
			'clientId': 'DCP-DISNEYSTORE.WEB-PROD',
			'scheme': 'https',
			'postMessageOrigin': 'https://www.shopdisney.com/minnie-mouse-the-main-attraction-ear-headband-for-adults-enchanted-tiki-room-limited-release-428405618185.html',
			'cookieDomain': 'www.shopdisney.com',
			'config': 'PROD',
			'logLevel': 'INFO',
			'topHost': 'www.shopdisney.com',
			'langPref': 'en-US',
			'cssOverride': 'https://static-mh.content.disney.io/catalog/assets/oneid-f61baacef5e1.css',
			'responderPage': 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/OneID-Responder',
			'buildId': '17175563986'
		}

		try:
			r = self.s.get(url, headers=self.headers, params=params)
		except Exception as e:
			print(f'{e}')

		print(r)
		# print(r.text)

	def add_to_cart(self):
		self.current_step = 0
		self.status = 'Adding to cart'
		# self.update_status.emit()
		print(f'''

============================================================
ADDING TO CART
============================================================

		''')
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
			print(data)
			# print(r.text)
			try:
				if data['quantityTotal'] > 0:
					self.shipmentUUID = data['cart']['items'][0]['shipmentUUID']
					self.shipping_ID = data['cart']['shipments'][0]['selectedShippingMethod']
					self.title = data['cart']['items'][0]['productName']
					# self.update_title.emit()
					self.price = data['cart']['items'][0]['price']['sales']['formatted']
					src = data['cart']['items'][0]['images']['small'][0]['url']
					self.src = f'http://{src.split("//")[-1]}'
					# self.update_image.emit()
					url = f'https://www.shopdisney.com/{self.pid}.html'
					self.link = self.s.get(url, headers=self.headers).url
					# self.update_size.emit()
					return True
				if data['isSoldOut']:
					self.status = 'Out of stock'
			except Exception as e:
				print(f'{e}')
		else:
			print(r.json())
			self.status = self.handle_status(r.status_code)

		# self.update_status.emit()
		print(self.status)
		return False

	# def validate_basket(self):
	# 	self.current_step = 1
	# 	self.status = 'Validating basket'
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/my-bag?validateBasket=1'
	# 	try:
	# 		r = self.s.get(url, headers=self.headers)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	return False

	# def validate_checkout(self):
	# 	self.current_step = 2
	# 	self.status = 'Validating checkout'
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/ocapi/cc/checkout?validateCheckout=1'
	# 	try:
	# 		r = self.s.get(url, headers=self.headers)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	return False

	def start_checkout(self):
		# self.current_step = 3
		self.status = 'Starting checkout'
		# self.update_status.emit()
		# print(self.status)
		print(f'''
============================================================
STARTING CHECKOUT
============================================================
		''')
		url = 'https://www.shopdisney.com/checkout'
		try:
			r = self.s.get(url, headers=self.headers)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'lxml')
			self.csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
			print(f'CSRF TOKEN: {self.csrf_token}')
			return True
		else:
			# print(r.text)
			self.status = self.handle_status(r.status_code)

		# self.update_status.emit()
		print(self.status)
		return False

	def submit_shipping(self):
		# self.current_step = 4
		self.status = 'Submitting shipping'
		# self.update_status.emit()
		print(f'''
============================================================
SUBMITTING SHIPPING
============================================================
		''')
		url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/CheckoutShippingServices-SubmitShipping'
		payload = {
			'originalShipmentUUID': self.shipmentUUID,
			'shipmentUUID': self.shipmentUUID,
			'dwfrm_shipping_shippingAddress_addressFields_country': 'US',
			'dwfrm_shipping_shippingAddress_addressFields_firstName': 'Mike',
			'dwfrm_shipping_shippingAddress_addressFields_lastName': 'Kim',
			'dwfrm_shipping_shippingAddress_addressFields_address1': '200 S Tennessee St',
			'dwfrm_shipping_shippingAddress_addressFields_address2': '',
			'dwfrm_shipping_shippingAddress_addressFields_postalCode': '30120',
			'dwfrm_shipping_shippingAddress_addressFields_city': 'Cartersville',
			'dwfrm_shipping_shippingAddress_addressFields_states_stateCode': 'GA',
			'dwfrm_shipping_shippingAddress_addressFields_phone': '7737081444',
			'shippingMethod': self.shipping_ID,
			'csrf_token': self.csrf_token
		}
		try:
			r = self.s.post(url, headers=self.headers, data=payload)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.total_price = data['order']['totals']['grandTotal'].strip('$')
			print(f'CHECKOUT PRICE: {self.total_price}')
			return True
		else:
			# print(r.text)
			self.status = gecko_utils.resolve_status(r.status_code)

		self.update_status.emit()
		print(self.status)
		return False

	# def captcha(self):
	# 	self.current_step = 5
	# 	self.status = 'Waiting for captcha'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	# Save cookies and send with along with emit signal
	# 	self.cookies = []
	# 	for cookie in self.s.cookies:
	# 		c = QtNetwork.QNetworkCookie()
	# 		c.setDomain(cookie.__dict__['domain'])
	# 		c.setName(bytes(cookie.__dict__['name'], 'utf-8'))
	# 		c.setValue(bytes(cookie.__dict__['value'], 'utf-8'))
	# 		self.cookies.append(c)
	# 	# Emit signal to load captcha and browser
	# 	self.request_captcha.emit()
	# 	# self.waiting_for_captcha = True
	# 	# while self.waiting_for_captcha:
	# 	while True:
	# 		if self.abort:
	# 			return False
	# 		else:
	# 			if self.g_recaptcha_response is None:
	# 				print('Waiting for captcha')
	# 				self.poll_response.emit()
	# 				time.sleep(1)
	# 			else:
	# 				return True

	# def google_recaptcha(self):
	# 	self.current_step = 6
	# 	self.status = 'Google recaptcha'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Google-reCaptcha'
	# 	payload = {
	# 		'dwfrm_billing_addressFields_firstName': self.profile.first_name,
	# 		'dwfrm_billing_addressFields_lastName': self.profile.last_name,
	# 		'dwfrm_billing_addressFields_address1': self.profile.billing_address,
	# 		'dwfrm_billing_addressFields_address2': self.profile.billing_address_2,
	# 		'dwfrm_billing_addressFields_country': 'US',
	# 		'dwfrm_billing_addressFields_states_stateCode': self.profile.billing_state,
	# 		'dwfrm_billing_addressFields_city': self.profile.billing_city,
	# 		'dwfrm_billing_addressFields_postalCode': self.profile.billing_zip,
	# 		'dwfrm_billing_paymentDetails': '',
	# 		'dwfrm_billing_commerceId': '',
	# 		'dwfrm_billing_vcoWalletRefId': '',
	# 		'dwfrm_billing_creditCardFields_email': self.profile.email,
	# 		'g-recaptcha-response': self.g_recaptcha_response
	# 	}
	# 	h = self.headers
	# 	h['content-type'] = 'application/x-www-form-urlencoded'
	# 	try:
	# 		r = self.s.post(url, headers=h, data=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def checkout_validate_basket(self):
	# 	self.current_step = 7
	# 	self.status = 'Checkout validating basket'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Checkout-ValidateBasket'
	# 	payload = {
	# 		'dwfrm_billing_addressFields_firstName': self.profile.first_name,
	# 		'dwfrm_billing_addressFields_lastName': self.profile.last_name,
	# 		'dwfrm_billing_addressFields_address1': self.profile.billing_address,
	# 		'dwfrm_billing_addressFields_address2': self.profile.billing_address_2,
	# 		'dwfrm_billing_addressFields_country': 'US',
	# 		'dwfrm_billing_addressFields_states_stateCode': self.profile.billing_state,
	# 		'dwfrm_billing_addressFields_city': self.profile.billing_city,
	# 		'dwfrm_billing_addressFields_postalCode': self.profile.billing_zip,
	# 		'dwfrm_billing_paymentDetails': '',
	# 		'dwfrm_billing_commerceId': '',
	# 		'dwfrm_billing_vcoWalletRefId': '',
	# 		'dwfrm_billing_creditCardFields_email': self.profile.email,
	# 		'g-recaptcha-response': self.g_recaptcha_response
	# 	}
	# 	h = self.headers
	# 	h['referer'] = 'https://www.shopdisney.com/checkout?stage=payment'
	# 	h['TE'] = 'Trailers'
	# 	try:
	# 		r = self.s.post(url, headers=h, data=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.order_number = data['orderID']
	# 		print(f'ORDER NUMBER: {self.order_number}')
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def auth_token(self):
	# 	self.current_step = 8
	# 	self.status = 'Auth token'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://authorization.go.com/token'
	# 	payload = {
	# 		'client_id': 'DSI-DISHOPWEB-PROD',
	# 		'grant_type': 'assertion',
	# 		'assertion_type': 'public'
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=self.headers, data=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		# print(data)
	# 		self.access_token = data['access_token']
	# 		self.bearer = data['token_type']
	# 		print(f'ACCESS TOKEN: {self.access_token}')
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def submit_billing(self):
	# 	self.current_step = 9
	# 	self.status = 'Submitting billing'
	# 	self.update_status.emit()
	# 	print(self.status)	
	# 	url = 'https://www.shopdisney.com/api/addresses'
	# 	h = self.headers
	# 	h['content-type'] = 'application/json'
	# 	h['Authorization'] = f'{self.bearer} {self.access_token}'
	# 	payload = {
	# 		'addresses': [
	# 			{
	# 				'address1': self.profile.billing_address,
	# 				'address2': self.profile.billing_address_2,
	# 				'city': self.profile.billing_city,
	# 				'country': 'US',
	# 				'first_name': self.profile.first_name,
	# 				'last_name': self.profile.last_name,
	# 				'phone1': self.profile.phone,
	# 				'state': self.profile.billing_state,
	# 				'type': 'SB',
	# 				'zip_code': self.profile.billing_zip
	# 			}
	# 		]
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=h, json=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		# print(data)
	# 		self.address_ID = data['addresses'][0]['address_id']
	# 		self.commerce_ID = data['commerce_id']
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def submit_order(self):
	# 	self.current_step = 10
	# 	self.status = 'Submitting order'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/api/orders'
	# 	h = self.headers
	# 	h['commerce_id'] = self.commerce_ID
	# 	h['authorization'] = f'{self.bearer} {self.access_token}'
	# 	h['content-type'] = 'application/json'
	# 	payload = {
	# 		'orders': [{
	# 			'description': 'GUEST|BAG',
	# 			'ext_order_id': self.order_number
	# 		}]
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=h, json=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.commerce_ID = data['commerce_id']
	# 		self.order_ID = data['orders'][0]['order_id']
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def submit_payment(self):
	# 	self.current_step = 11
	# 	self.status = 'Submitting payment'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = f'https://www.shopdisney.com/api/orders/{self.order_ID}/payments'
	# 	h = self.headers
	# 	h['commerce_id'] = self.commerce_ID
	# 	h['authorization'] = f'{self.bearer} {self.access_token}'
	# 	h['content-type'] = 'application/json'
	# 	payload = {
	# 		'payments': [{
	# 			'address': {
	# 				'address_id': self.address_ID
	# 			},
	# 			'card_brand': 'VS',
	# 			'card_number': self.billing.card_number,
	# 			'expiration_month': self.billing.exp_month,
	# 			'expiration_year': self.billing.exp_year,
	# 			'is_expired': False,
	# 			'name_holder': self.billing.name_on_card,
	# 			'payment_id': '',
	# 			'security_code': self.billing.cvv,
	# 			'type': 'CC'
	# 		}]
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=h, json=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		# print(data)
	# 		self.commerce_ID = data['commerce_id']
	# 		self.payment_ID = data['payments'][0]['payment_id']
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def get_order(self):
	# 	self.current_step = 12
	# 	self.status = 'Getting order'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = f'https://www.shopdisney.com/api/orders/{self.order_ID}'
	# 	# url = f'https://www.shopdisney.com/api/v2/orders/{self.order_number}'
	# 	h = self.headers
	# 	h['commerce_id'] = self.commerce_ID
	# 	h['authorization'] = f'{self.bearer} {self.access_token}'
	# 	h['content-type'] = 'application/json'
	# 	try:
	# 		r = self.s.get(url, headers=h)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.commerce_ID = data['commerceId']
	# 		self.payment_details = json.dumps(data['orders'][0]['payments'])
	# 		print(self.payment_details)
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def verify_order(self):
	# 	self.current_step = 13
	# 	self.status = f'Veryifing order: {self.order_number}'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = f'https://www.shopdisney.com/api/v2/orders/{self.order_number}'
	# 	h = self.headers
	# 	h['commerce_id'] = self.commerce_ID
	# 	h['authorization'] = f'{self.bearer} {self.access_token}'
	# 	h['content-type'] = 'application/json'
	# 	payload = {
	# 		'orders': [{
	# 			'order_total': self.total_price,
	# 			'payments': [{
	# 				'payment_id': self.payment_ID,
	# 				'security_code': self.billing.cvv,
	# 				'type': 'CC'
	# 			}]
	# 		}]
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=h, json=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.commerce_ID = data['commerce_id']
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def checkout_submit_order(self):
	# 	self.current_step = 14
	# 	self.status = 'Submitting order'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/on/demandware.store/Sites-shopDisney-Site/default/Checkout-SubmitOrder'
	# 	payload = {
	# 		'dwfrm_billing_addressFields_firstName': self.profile.first_name,
	# 		'dwfrm_billing_addressFields_lastName': self.profile.last_name,
	# 		'dwfrm_billing_addressFields_address1': self.profile.billing_address,
	# 		'dwfrm_billing_addressFields_address2': self.profile.billing_address_2,
	# 		'dwfrm_billing_addressFields_country': 'US',
	# 		'dwfrm_billing_addressFields_states_stateCode': self.profile.billing_state,
	# 		'dwfrm_billing_addressFields_city': self.profile.billing_city,
	# 		'dwfrm_billing_addressFields_postalCode': self.profile.billing_zip,
	# 		'dwfrm_billing_paymentDetails': self.payment_details,
	# 		'dwfrm_billing_commerceId': self.commerce_ID,
	# 		'dwfrm_billing_vcoWalletRefId': '',
	# 		'dwfrm_billing_creditCardFields_email': self.profile.email,
	# 		'dwfrm_billing_subscribe': 'on',
	# 		'g-recaptcha-response': self.g_recaptcha_response
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=self.headers, data=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.order_number = data['orderID']
	# 		self.order_token = data['orderToken']

	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def order_confirmation(self):
	# 	self.current_step = 15
	# 	self.status = 'Getting order confirmation'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	url = 'https://www.shopdisney.com/ocapi/cc/orderconfirmation'
	# 	payload = {
	# 		'order_number': self.order_number,
	# 		'order_token': self.order_token
	# 	}
	# 	try:
	# 		r = self.s.post(url, headers=self.headers, data=payload)
	# 	except Exception as e:
	# 		print(f'{e}')
	# 		return False

	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		return True
	# 	else:
	# 		# print(r.text)
	# 		self.status = gecko_utils.resolve_status(r.status_code)

	# 	self.update_status.emit()
	# 	print(self.status)
	# 	return False

	# def submit_webhook(self):
	# 	self.current_step = 16
	# 	self.status = f'Check email! Order #: {self.order_number}'
	# 	self.update_status.emit()
	# 	print(self.status)
	# 	try:
	# 		gecko_utils.post_webhook(self.title, self.store, self.link, self.price, self.qty, self.src, self.color, self.size)
	# 	except Exception as e:
	# 		print(f'{e}')

	# 	return True

store = Disney()
# store.get_page()
store.add_to_cart()
# store.start_checkout()
# store.submit_shipping()