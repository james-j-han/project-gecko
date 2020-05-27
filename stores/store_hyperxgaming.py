from bs4 import BeautifulSoup

import requests
import json
import time

# VERSION 0.1
class HyperXGaming:

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

	def __init__(self, profile):
		self.s = requests.Session()
		self.profile = profile

		# Product info
		self.session_ID = None
		self.verification_token = None
		self.promo_code = None
		self.stripe_key = 'pk_live_GiSktffRI3h9Z05kpLUWEIVi'
		self.stripe_token = None

		# Other info
		self.status = 'Ready'
		self.current_step = 0
		self.steps = [
			self.add_to_cart,
			self.get_session,
			self.submit_shipping,
			self.submit_billing,
			self.check_city_state_zip,
			self.submit_order
		]

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

	# def go_to_site(self):
	# 	url = 'https://m.stripe.com/4'
	# 	payload = {
	# 		 'JTdCJTIybXVpZCUyMiUzQSUyMjgxMWRjZjA2LTNjYzktNDkyNS04MDlmLTM4MDdjNzA4Y2IzYyUyMiUyQyUyMnNpZCUyMiUzQSUyMjE3ZWI0ZDMxLTYwOWItNGEwZC04MWEyLTA0MzhjZTcxMzE1YyUyMiUyQyUyMnVybCUyMiUzQSUyMmh0dHBzJTNBJTJGJTJGd3d3Lmh5cGVyeGdhbWluZy5jb20lMkZ1cyUyMiUyQyUyMnNvdXJjZSUyMiUzQSUyMm1vdXNlLXRpbWluZ3MtMTAlMjIlMkMlMjJkYXRhJTIyJTNBJTVCOTQyMDclMkMzJTJDMTUlMkMxMCUyQzclMkM5JTJDOCUyQzclMkM0OTQlMkM3JTVEJTdE': ''
	# 	}
	# 	r = self.s.post(url, headers=self.headers, data=payload)
	# 	print(r)
	# 	url = 'https://www.hyperxgaming.com/us/shop/basket/getbaskets'
	# 	payload = {
	# 		'SessionID': '',
	# 		'v': int(time.time())
	# 	}
	# 	r = self.s.get(url, headers=self.headers, data=payload)
	# 	print(r)
	# 	for cookie in self.s.cookies:
	# 		print(cookie)
	# 	for cookie in r.cookies:
	# 		print(cookie)

	def add_to_cart(self):
		self.current_step = 0
		self.status = 'Adding to cart'
		print(self.status)
		url = 'https://www.hyperxgaming.com/us/shop/basket'
		payload = {
			'partNumber': self.profile.sku,
			'quantity': self.profile.qty
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
			self.session_ID = data['Result']['SessionID']
			print(f'Session ID: {self.session_ID}')
			print(len(self.session_ID))
			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

	def get_session(self):
		self.current_step = 1
		self.status = 'Getting session'
		print(self.status)
		url = 'https://www.hyperxgaming.com/us/shop/order/checkout'
		try:
			r = self.s.get(url, headers=self.headers)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			soup = BeautifulSoup(r.text, 'html.parser')
			# self.session_ID = soup.find('input', {'id': 'SessionID'})['value']
			self.verification_token = soup.find_all('input', {'name': '__RequestVerificationToken'})[-1]['value']
			self.promo_code = soup.find('input', {'id': 'PromoCode'})['value']
			# print(f'Session ID: {self.session_ID}')
			print(f'Verification TOKEN: {self.verification_token}')
			print(f'Promo CODE: {self.promo_code}')
			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

	def submit_shipping(self):
		self.current_step = 2
		self.status = 'Submitting shipping'
		print(self.status)
		url = 'https://www.hyperxgaming.com/us/shop/order/getpaymentinfo'
		payload =  {
			'ShipCountry': self.profile.country,
			'ShipMethod': 'RPN',
			'ShipCity': self.profile.s_city,
			'ShipState': self.profile.s_state,
			'ShipZip': self.profile.s_zip,
			'SessionID': self.session_ID,
			'PromoCode': self.promo_code,
			'v': int(time.time())
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
			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

	def submit_billing(self):
		self.current_step = 3
		self.status = 'Submitting billing'
		print(self.status)
		url = 'https://api.stripe.com/v1/tokens'
		payload = {
			'card[name]': self.profile.card_name,
			'card[address_line1]': self.profile.b_address,
			'card[address_line2]': self.profile.b_address_2,
			'card[address_city]': self.profile.b_city,
			'card[address_state]': self.profile.b_state,
			'card[address_zip]': self.profile.b_zip,
			'card[address_country]': 'US',
			'card[number]': self.profile.card_number,
			'card[cvc]': self.profile.card_cvv,
			'card[exp_month]': self.profile.card_month,
			'card[exp_year]': self.profile.card_year,
			# 'guid': '',
			# 'muid': '',
			# 'sid': '',
			# 'payment_user_agent': 'stripe.js/8b044688;+stripe-js-v3/8b044688',
			# 'time_on_page': '189619',
			'referrer': 'https://www.hyperxgaming.com/us/shop/order/checkout',
			'key': self.stripe_key
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
			self.stripe_token = data['id']
			print(self.stripe_token)
			for cookie in self.s.cookies:
				print(cookie)
			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

	def check_city_state_zip(self):
		self.current_step = 4
		self.status = 'Checking city, state, and zip'
		print(self.status)
		url = 'https://www.hyperxgaming.com/us/shop/order/checkcitystatezip'
		payload = {
			'BillCity': self.profile.b_city,
			'BillState': self.profile.b_state,
			'BillZip': self.profile.b_zip,
			'SameAsShippingAddress': False,
			'SessionID': self.session_ID,
			'ShipCity': self.profile.s_city,
			'ShipState': self.profile.s_state,
			'ShipZip': self.profile.s_zip
		}
		h = self.headers
		h['Content-Type'] = 'application/json;'
		try:
			r = self.s.post(url, headers=h, json=payload)
		except Exception as e:
			print(f'{e}')
			return False

		print(r)
		if r.status_code == 200:
			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

	def submit_order(self):
		self.current_step = 5
		self.status = 'Submitting order'
		url = 'https://www.hyperxgaming.com/us/shop/order/checkout'
		payload = {
			'Action': 'New',
			'PaymentGateway': 2,
			'PayMethod': '',
			'PayerToken': self.stripe_token,
			'SessionID': self.session_ID,
			'CustomerID': '',
			'PromoCode': self.promo_code,
			'Email': self.profile.email,
			'CompanyName': '',
			'Country': self.profile.country,
			'FirstName': self.profile.s_first_name,
			'LastName': self.profile.s_last_name,
			'Phone': self.profile.phone,
			'Fax': '',
			'ShipAttentionCompany': '',
			'ShipAddress3': '',
			'ShipCountry': self.profile.country,
			'BillAttentionCompany': '',
			'BillAddress3': '',
			'BillCountry': self.profile.country,
			'BillPhone': '',
			'ShipAttentionFirstName': self.profile.s_first_name,
			'ShipAttentionLastName': self.profile.s_last_name,
			'ShipAddress1': self.profile.s_address,
			'ShipAddress2': self.profile.s_address_2,
			'ShipCity': self.profile.s_city,
			'ShipState': self.profile.s_state,
			'ShipZip': self.profile.s_zip,
			'ShipPhone': self.profile.phone,
			'ShipMethod': 'RPN',
			'SameAsShippingAddress': False,
			'BillAttentionFirstName': self.profile.b_first_name,
			'BillAttentionLastName': self.profile.b_last_name,
			'BillAddress1': self.profile.b_address,
			'BillAddress2': self.profile.b_address_2,
			'BillCity': self.profile.b_city,
			'BillState': self.profile.b_state,
			'BillZip': self.profile.b_zip,
			'ecommerceQuantity': self.profile.qty,
			'DiscountCode2': '',
			'__RequestVerificationToken': self.verification_token
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

			return True
		else:
			self.handle_status(r.status_code)

		print(self.status)
		return False

# Edit personal info here
class Profile:

	def __init__(self):
		# self.sku = 'HX-MC005B'
		# self.sku = 'HKBDXM-1C-US/G'
		self.sku = 'HX-MPFS-SM'
		self.qty = 1
		self.email = 'dummy@gmail.com'
		self.phone = '6789554481'
		self.country = 'US'
		self.s_first_name = 'John'
		self.s_last_name = 'Doe'
		self.s_address = '200 Main St'
		self.s_address_2 = ''
		self.s_city = 'Cartersville'
		self.s_state = 'GA'
		self.s_zip = '30120'
		self.b_first_name = 'John'
		self.b_last_name = 'Doe'
		self.b_address = '200 Main St'
		self.b_address_2 = ''
		self.b_city = 'Cartersville'
		self.b_state = 'GA'
		self.b_zip = '30120'
		self.card_name = 'John Doe'
		self.card_number = '4833130037625522'
		self.card_month = '9'
		self.card_year = '2022'
		self.card_cvv = '323'

# Setup and main loop
# profile = Profile()
# store = HyperXGaming(profile)
# store.go_to_site()
# store.add_to_cart()
# store.get_session()
# store.submit_shipping()
# store.submit_billing()
# store.check_city_state_zip()
# store.submit_order()

# for step in store.steps[store.current_step:]:
# 	if step():
# 		continue
# 	else:
# 		break