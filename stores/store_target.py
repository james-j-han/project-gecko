from PyQt5.QtCore import QObject, pyqtSignal, QByteArray
from PyQt5 import QtCore, QtNetwork

import requests
import gecko_utils

class Target(QObject):

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
	}

	def __init__(self, search, qty, size, color, account, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.proxy = None
		self.tcin = search
		self.account = account
		self.profile = profile
		self.billing = billing

		self.cart_id = None
		self.payment_instruction_id = None

		# Webhook info
		self.store = 'https://www.target.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size

		self.status = 'Ready'

		self.steps = [
			self.step_1,
			self.step_2,
			self.step_3,
			self.step_4,
			self.step_5,
			self.step_6
		]

	def step_1(self):
		url = 'https://gsp.target.com/gsp/authentications/v1/auth_codes?client_id=ecom-web-1.0.0&state=1585456116676&redirect_uri=https%3A%2F%2Fwww.target.com%2F&assurance_level=M'

	def step_2(self):
		self.status = 'Searching for product'
		url = f'https://redsky.target.com/v3/pdp/tcin/{self.tcin}'
		params = {
			'excludes': 'taxonomy,bulk_ship,awesome_shop,question_answer_statistics,rating_and_review_reviews,rating_and_review_statistics,deep_red_labels,in_store_location',
			'key': 'eb2551e4accc14f38cc42d32fbc2b2ea'
		}
		r = requests.get(url, headers=self.headers, params=params, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			self.title = data['product']['item']['product_description']['title']
			self.link = data['product']['item']['buy_url']
			image_url = data['product']['item']['enrichment']['images'][0]
			self.src = f'{image_url["base_url"]}{image_url["primary"]}'
			return True
		
		self.status = 'Could not find product'
		return False

	def step_3(self):
		self.status = 'Adding to cart'
		# Returns carted item details (not full cart)
		url = 'https://carts.target.com/web_checkouts/v1/cart_items'
		headers = {
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'x-application-name': 'web'
		}
		payload = {
			'cart_type': 'REGULAR',
			'channel_id': '90',
			'shopping_context': 'DIGITAL',
			'cart_item': {
				'tcin': self.tcin,
				'quantity': self.qty,
				'item_channel_id': '10'
			}
		}
		params = {
			'field_groups': 'CART,CART_ITEMS,SUMMARY',
			'key': 'feaf228eb2777fd3eee0fd5192ae7107d6224b39'
		}
		r = self.s.post(url, headers=headers, json=payload, params=params, proxies=self.proxy)
		print(r)
		if r.status_code == 201:
			data = r.json()
			print(data)
			self.cart_id = data['cart_id']
			self.price = data['item_summary']['total_product']
			return True
		elif r.status_code == 424:
			self.status = 'Out of stock'
		elif r.status_code == 401:
			print('[401]: Unauthorized')
		
		self.status = 'Could not cart'
		return False

	def step_4(self):
		self.status = 'Starting checkout'
		url = 'https://carts.target.com/web_checkouts/v1/pre_checkout'
		headers = {
			'accept': 'application/json',
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'x-application-name': 'web'
		}
		params = {
			'field_groups': 'ADDRESSES,CART,CART_ITEMS,DELIVERY_WINDOWS,PAYMENT_INSTRUCTIONS,PICKUP_INSTRUCTIONS,PROMOTION_CODES,SUMMARY',
			'key': 'feaf228eb2777fd3eee0fd5192ae7107d6224b39'
		}
		payload = {
			'cart_type': 'REGULAR'
		}
		r = self.s.post(url, headers=headers, params=params, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 201:
			data = r.json()
			print(data)
			self.payment_instruction_id = data['payment_instructions'][0]['payment_instruction_id']
			return True
		
		return False

	def step_5(self):
		self.status = 'Applying billing'
		# payment_instruction_id
		url = f'https://carts.target.com/checkout_payments/v1/payment_instructions/{self.payment_instruction_id}'
		headers = {
			'accept': 'application/json',
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'x-application-name': 'web'
		}
		params = {
			'key': 'feaf228eb2777fd3eee0fd5192ae7107d6224b39'
		}
		payload = {
			'billing_address': {
				'address_line1': self.profile.billing_address,
				'address_line2': self.profile.billing_address_2,
				'city': self.profile.billing_city,
				'country': 'US',
				'first_name': self.profile.first_name,
				'last_name': self.profile.last_name,
				'phone': self.profile.phone,
				'state': self.profile.billing_state,
				'zip_code': self.profile.billing_zip,
			},
			'card_details': {
				'card_name': self.billing.name_on_card,
				'card_number': self.billing.card_number,
				'cvv': self.billing.cvv,
				'expiry_month': self.billing.exp_month,
				'expiry_year': self.billing.exp_year
			},
			'cart_id': self.cart_id,
			'payment_type': 'CARD',
			# 'wallet_card_id': '',
			'wallet_mode': 'ADD' # GET
		}
		r = self.s.put(url, headers=headers, params=params, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True
		
		return False

	def step_6(self):
		self.status = 'Submitting payment'
		url = 'https://carts.target.com/web_checkouts/v1/checkout'
		headers = {
			'accept': 'application/json',
			'content-type': 'application/json',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'x-application-name': 'web'
		}
		params = {
			'field_groups': 'ADDRESSES,CART,CART_ITEMS,DELIVERY_WINDOWS,PAYMENT_INSTRUCTIONS,PICKUP_INSTRUCTIONS,PROMOTION_CODES,SUMMARY',
			'key': 'feaf228eb2777fd3eee0fd5192ae7107d6224b39'
		}
		payload = {
			'cart_type': 'REGULAR',
			'channel_id': 10
		}
		r = self.s.post(url, headers=headers, params=params, json=payload, proxies=self.proxy)
		print(r)
		if r.status_code == 200:
			data = r.json()
			print(data)
			return True
		
		return False

	def verify_checkout(self):
		gecko_utils.post_webhook(self.title, self.store, self.link, self.price, self.qty, self.src, self.color, self.size)
		return True

	# def get_cart(self):
	# 	print('Getting cart')
	# 	url = 'https://carts.target.com/web_checkouts/v1/cart_views'
	# 	# url = 'https://carts.target.com/web_checkouts/v1/cart'
	# 	headers = {
	# 		'accept': 'application/json',
	# 		'content-type': 'application/json',
	# 		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
	# 		'x-application-name': 'web'
	# 	}
	# 	params = {
	# 		'cart_type': 'REGULAR',
	# 		'field_groups': 'CART,CART_ITEMS,SUMMARY,PROMOTION_CODES,ADDRESSES',
	# 		'key': 'feaf228eb2777fd3eee0fd5192ae7107d6224b39',
	# 		'refresh': 'true'
	# 	}
	# 	r = self.s.get(url, headers=headers, params=params)
	# 	print(r)
	# 	data = r.json()
	# 	self.cart_id = data['cart_id']
	# 	print(data)