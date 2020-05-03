from PyQt5.QtCore import QObject, pyqtSignal

import requests
import gecko_utils
import json

class BestBuy(QObject):

	update_status = pyqtSignal(str)
	update_title = pyqtSignal(str)
	update_image = pyqtSignal(str)

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
	}

	def __init__(self, search, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.proxy = None
		self.sku = search
		# self.account = account
		self.profile = profile
		self.billing = billing

		# Webhook info
		self.store = 'https://www.bestbuy.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		self.status = 'Ready'
		self.abck = None

		self.steps = [
			self.step_0,
			self.step_1,
			# self.step_2,
			# self.step_3,
			# self.step_4,
			self.step_5,
			# self.step_6,
			self.step_7,
			# self.step_8,
			self.step_9,
			self.step_10,
			self.step_11,
			self.step_12,
			self.step_13,
		]

		self.cart_id = None
		self.line_id = None
		self.token = None
		self.order_id = None
		self.threeDS = None
		self.public_key = None
		self.key_id = None

	def set_cookies(self, cookie_jar):
		if self.abck:
			print('ABCK cookie already set')
		else:
			self.s = requests.Session()
			for cookie in cookie_jar.allCookies():
				name = cookie.name().data().decode()
				value = cookie.value().data().decode()
				domain = cookie.domain()
				if '_abck' in name:
					self.abck = value
					a = 'A3D1F2C269A37F4482C5AA11F29B8AE2~0~YAAQROotF3FIWYFxAQAAefq2ogOrvRAUseWjLAaluX7XCp1TVBZn5zXEaH5GYbw/WdZSkzTwXAhEUtYXcjjFrlFWFHobmUG/8w3kximbjndQ9orLmXwkmqNIMS+1aFOyIpMKjTpP557J0d8Ji7viBrMox9n2Iu33hZ5iYt5IWJu8Z9xf1e6VIIl3Vjhk8dZ2HtVIGnoahXfCwVvjJFxb4Dl1jtwFOcK8/zFzahlRsoUR2FyP+mkk556FEkbmiZMrf3zo7loMMaGLZ7d9l9D0qDquHDJF5xtjdKZwrL6jFohuEjqLpDWHQ8F8d+Mr6WW8sfjiRTNSqkQ=~-1~1-geLkrPIVuD-10000-100-3000-1||||~-1'
					self.s.cookies.set(name, a, domain=domain)

	def step_0(self):
		# self.status = 'Checking stock'
		# print(self.status)
		# url = 'https://www.bestbuy.com/api/tcfb/model.json'
		# params = {
		# 	'paths': json.dumps([
		# 		["shop", "scds", "v2", "page", "tenants", "bbypres", "pages", "globalnavigationv5sv", "header"],
		# 		["shop", "buttonstate", "v5", "item", "skus", f'{self.sku}', "conditions", "NONE", "destinationZipCode", "%20", "storeId", "%20", "context", "cyp", "addAll", "false"]
		# 		]),
		# 	'method': 'get'
		# }
		# r = self.s.get(url, params=params, headers=self.headers, proxies=self.proxy)
		# print(r)
		# if r.status_code == 200:
		# 	data = r.json()
		# 	print(data)
		# 	if 'ADD_TO_CART' in r.text:
		# 		return True

		# status = 'Waiting for restock'
		# return False
		if self.abck is None:
			self.status = 'Generating Akamai Cookie'
			self.update_status.emit(self.status)
			print(self.status)
			jar = gecko_utils.gen_akamai()
			self.s.cookies.set(jar['name'], jar['value'], domain=jar['domain'])
			self.abck = jar

		return True

	def step_1(self):
		self.status = 'Checking cart'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/basket/v1/basketCount'
		h = self.headers
		h['X-CLIENT-ID'] = 'browse'
		h['X-REQUEST-ID'] = 'global-header-cart-count'
		r = self.s.get(url, headers=h, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			if data['count'] > 0:
				return True

		self.status = 'Adding to cart'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/cart/api/v1/addToCart'
		payload = {
			'items': [{
				'skuId': self.sku
			}]
		}
		try:
			r = self.s.post(url, headers=self.headers, json=payload, proxies=self.proxy, timeout=(3, 3))
		except Exception as e:
			print(f'{e}')
			self.abck = None
			return False
			
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.line_id = data['summaryItems'][0]['lineId']
			self.price = data['summaryItems'][0]['price']
			self.cart_info()
			return True
		elif r.status_code == 400:
			data = r.json()
			# print(data)
			self.status = 'Unavailable'
			self.update_status.emit(self.status)
			error = data['errorSummary']
			print(f'[400]: {error}')

		self.status = 'Could not cart'
		self.update_status.emit(self.status)
		return False

	# def step_2(self):
	# 	self.status = 'Getting cart id'
	# 	print(self.status)
	# 	url = 'https://www.bestbuy.com/basket/v1/basket'
	# 	h = self.headers
	# 	h['X-CLIENT-ID'] = 'not null'
	# 	r = self.s.get(url, headers=h, proxies=self.proxy)
	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.cart_id = data['id']
	# 		return True

	# 	return False

	def cart_info(self):
		self.status = 'Getting cart info'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/cart/json'
		h = self.headers
		# h['X-ORDER-ID'] = self.cart_id
		h['X-ORDER-ID'] = 'undefined'
		r = self.s.get(url, headers=h, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.src = data['cart']['lineItems'][0]['item']['imageUrl']
			path = data['cart']['lineItems'][0]['item']['itemUrl']
			self.link = f'https://www.bestbuy.com{path}'
			self.update_image.emit(self.link)
			self.title = data['cart']['lineItems'][0]['item']['shortLabel']
			self.update_title.emit(self.title)
			self.order_id = data['cart']['id']
			# return True
		else:
			pprint(r.text)

		self.status = 'Cart error'
		self.update_status.emit(self.status)
		# return False

	# def step_4(self):
	# 	self.status = 'Selecting shipping option'
	# 	print('Selecting shipping')
	# 	h = self.headers
	# 	h['X-ORDER-ID'] = self.cart_id
	# 	payload = {
	# 		'selected': 'SHIPPING'
	# 	}
	# 	url = f'https://www.bestbuy.com/cart/item/{self.line_id}/fulfillment'
	# 	r = self.s.put(url, headers=h, json=payload, proxies=self.proxy)
	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		self.fulfillment_type = data['order']['lineItems'][0]['item']['fulfillmentType']
	# 		print(self.fulfillment_type)
	# 		if 'shipping' in self.fulfillment_type:
	# 			return True

	# 	self.status = 'In store pickup only'
	# 	return False

	# def step_5(self):
	# 	self.status = 'Starting checkout'
	# 	print('Starting checkout')
	# 	url = 'https://www.bestbuy.com/cart/d/checkout'
	# 	h = self.headers
	# 	h['X-ORDER-ID'] = self.cart_id
	# 	payload = {}
	# 	r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.token = data['updateData']['order']['ciaToken']
	# 		return True
	# 	elif r.status_code == 412:
	# 		try:
	# 			alert = data['updateData']['order']['alerts']
	# 			print(alert)
	# 		except:
	# 			print('Could not get error summary')
	# 		self.status = 'Unavailable'

	# 	self.status = 'Unavailable'
	# 	return False

	def step_5(self):
		self.status = 'Starting checkout'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/checkout/r/fufillment'
		r = self.s.get(url, headers=self.headers, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			return True
		else:
			print(r.text)

		self.status = 'Checkout error'
		self.update_status.emit(self.status)
		return False

	# def step_6(self):
	# 	print('Checking out as guest')
	# 	url = 'https://www.bestbuy.com/identity/guest'
	# 	params = {
	# 		'token': self.token
	# 	}
	# 	r = self.s.get(url, headers=self.headers, params=params, proxies=self.proxy)
	# 	print(r)
	# 	if r.status_code == 200:
	# 		return True

	# 	return False

	def step_7(self):
		self.status = 'Applying shipping info'
		self.update_status.emit(self.status)
		print('Applying shipping info')
		url = f'https://www.bestbuy.com/checkout/orders/{self.order_id}/'
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
							'city': self.profile.shipping_city,
							'country': 'US',
							'dayPhoneNumber': self.profile.phone,
							'firstName': self.profile.first_name,
							'isWishListAddress': False,
							'lastName': self.profile.last_name,
							'middleInitial': '',
							'override': False,
							'saveToProfile': False,
							'state': self.profile.shipping_state,
							'street': self.profile.shipping_address,
							'street2': self.profile.shipping_address_2,
							'type': 'RESIDENTIAL',
							'useAddressAsBilling': False,
							'zipcode': self.profile.shipping_zip,
							'emailAddress': self.profile.email,
							'phoneNumber': self.profile.phone,
							'smsNotifyNumber': '',
							'smsOptIn': False
						}
					}
				}
			}]
		}
		r = self.s.patch(url, headers=h, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return False
		elif r.status_code == 400:
			data = r.json()
			print(data['errors'][0])
		else:
			print(r.text)

		self.status = 'Error applying shipping info'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	# def step_8(self):
	# 	print('Applying guest info')
	# 	url = f'https://www.bestbuy.com/checkout/orders/{self.cart_id}/'
	# 	h = self.headers
	# 	h['X-User-Interface'] = 'DotCom-Optimized'
	# 	payload = {
	# 		'emailAddress': self.profile.email,
	# 		'phoneNumber': self.profile.phone,
	# 		'smsNotifyNumber': '',
	# 		'smsOptIn': False
	# 	}
	# 	r = self.s.patch(url, headers=h, json=payload, proxies=self.proxy)
	# 	print(r)
	# 	if r.status_code == 200:
	# 		data = r.json()
	# 		print(data)
	# 		self.order_id = data['customerOrderId']
	# 		return True

	# 	return False

	def step_9(self):
		self.status = 'TAS'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/api/csiservice/v2/key/tas'
		r = self.s.get(url, headers=self.headers, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.public_key = data['publicKey']
			self.key_id = data['keyId']
			return True

		self.status = 'TAS error'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def step_10(self):
		self.status = 'Applying payment info'
		self.update_status.emit(self.status)
		print(self.status)
		bin_number = self.billing.card_number[:6]
		number = gecko_utils.get_encrypted_card(self.public_key, self.billing.card_number, self.key_id)
		url = f'https://www.bestbuy.com/checkout/orders/{self.order_id}/paymentMethods'
		h = self.headers
		h['X-User-Interface'] = 'DotCom-Optimized'
		payload = {
			'billingAddress': {
				'city': self.profile.billing_city,
				'country': 'US',
				'dayPhoneNumber': self.profile.phone,
				'firstName': self.profile.first_name,
				'isWishListAddress': False,
				'lastName': self.profile.last_name,
				'middleInitial': '',
				'override': False,
				'saveToProfile': False,
				'state': self.profile.billing_state,
				'street': self.profile.billing_address,
				'street2': self.profile.billing_address_2,
				'useAddressAsBilling': True,
				'zipcode': self.profile.billing_zip
			},
			'creditCard': {
				'binNumber': bin_number,
				'cardType': self.billing.card_type,
				'cid': self.billing.cvv,
				'expiration': {
					'month': self.billing.exp_month,
					'year': self.billing.exp_year
				},
				'govPurchaseCard': False,
				'hasCID': True,
				'invalidCard': False,
				'isCustomerCard': False,
				'isInternationalCard': False,
				'isNewCard': True,
				'isPWPRegistered': False,
				'isVisaCheckout': False,
				'number': number
			}
		}
		r = self.s.patch(url, headers=h, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			# return True
			return True
		else:
			print(r.text)

		self.status = 'Error applying payment info'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def step_11(self):
		self.status = '3DSecure'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/payment/api/v1/threeDSecure/preLookup'
		h = self.headers
		h['X-CLIENT'] = 'CHECKOUT'
		payload = {
			'binNumber': bin_number,
			'browserInfo': {
				'colorDepth': '24',
				'height': '1920',
				'width': '1080',
				'javaEnabled': 'false',
				'language': 'en-US',
				'timeZone': '240',
				'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
			},
			'orderId': self.order_id
		}
		r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.threeDS = data['threeDSReferenceId']
			return True
		else:
			print(r.text)

		self.status = '3DSecure error'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def step_12(self):
		self.status = 'Submitting payment'
		self.update_status.emit(self.status)
		print(self.status)
		url = 'https://www.bestbuy.com/checkout/api/1.0/paysecure/submitCardAuthentication'
		h = self.headers
		h['X-Native-Checkout-Version'] = '__VERSION__'
		h['X-User-Interface'] = 'DotCom-Optimized'
		payload = {
			'orderId': self.order_id,
			'threeDSecureStatus': {
				'threeDSReferenceId': self.threeDS
			}
		}
		r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			return True
		else:
			print(r.text)
		
		self.status = 'Error submitting payment'
		self.update_status.emit(self.status)
		print(self.status)
		return False

	def step_13(self):
		self.status = 'Verifying order'
		self.update_status.emit(self.status)
		print(self.status)
		url = f'https://www.bestbuy.com/checkout/orders/{self.order_id}/'
		h = self.headers
		h['X-User-Interface'] = 'DotCom-Optimized'
		payload = {
			'browserInfo': {
				'colorDepth': '24',
				'height': '1920',
				'width': '1080',
				'javaEnabled': 'false',
				'language': 'en-US',
				'timeZone': '240',
				'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
			}
		}
		r = self.s.post(url, headers=h, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			state = data['state']
			if 'submitted' in state.lower():
				self.status = 'Order placed. Check your email.'
				self.update_status.emit(self.status)
				print(self.status)
				try:
					gecko_utils.post_webhook(self.title, self.store, self.link, self.price, self.qty, self.src, self.color, self.size)
				except Exception as e:
					print(f'{e}')
			return True

		self.status = 'Error verifying order'
		print(self.status)
		return False