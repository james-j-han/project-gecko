from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import os
import json
import time
import base64
import random
import requests
import datetime
import urllib.parse

def get_sitekey(html):
	soup = BeautifulSoup(html, 'html.parser')
	div = soup.find('div', {'class': 'g-recaptcha-nojs'})
	try:
		sitekey = div.iframe['src'].split('=')[-1]
		print('    [SITEKEY]: {}'.format(sitekey))
	except:
		sitekey = None
	return sitekey

def detect_captcha(html):
	soup = BeautifulSoup(html, 'html.parser')
	captcha = soup.find('textarea', id='g-recaptcha-response')
	if captcha:
		print('    [CAPTCHA]: Detected')
		return True
	else:
		print('    [CAPTCHA]: No captcha')
		return False

def get_random_client_resolution():
	resolution = {}
	resolution['width'] = random.randint(800, 1921)
	resolution['height'] = random.randint(600, 1081)
	print('[RESOLUTION]: {}x{}'.format(resolution['width'], resolution['height']))
	return resolution

def capture_response(folder, file_name, content):
	if not os.path.exists('{}'.format(folder)):
		os.makedirs('{}'.format(folder))
	if type(content) == dict:
		outfile = json.dumps(content, sort_keys=True, ensure_ascii=False)
	else:
		outfile = content
	try:
		path = '{}/{}'.format(folder, file_name)
		with open(path, mode='w', encoding='utf-8') as f:
			f.write(outfile)
		print('    [CAPTURE RESPONSE]: SUCCESS')
	except Exception as e:
		print('[EXCEPTION]: {}'.format(e))

def get_final_price(html):
	soup = BeautifulSoup(html, 'html.parser')
	final_price = soup.find('span', {'class': 'total-recap__final-price'})['data-checkout-payment-due-target']
	print('    [FINAL PRICE]: {}'.format(final_price))
	return final_price

def get_checkout_price(subtotal, postal):
	endpoint_sandbox = 'https://sandbox-rest.avatax.com/api/v2/taxrates/bypostalcode'
	endpoint_production = 'https://rest.avatax.com/api/v2/taxrates/bypostalcode'
	headers = {
		'Authorization': 'Basic MjAwMDE3MDQzNDo0MDkxNTA0Q0FERUE4RDc2',
		'Accept': 'application/json',
		'Method': 'GET'
	}
	params = {
		'country': 'United States',
		'postalCode': postal
	}
	r = requests.get(endpoint_production, headers=headers, params=params).json()
	tax_rate = r['totalRate']
	tax = round(subtotal * tax_rate, 2)
	total = int((subtotal + tax) * 100)
	print('    [CHECKOUT PRICE]: {}'.format(total))
	return total

def get_shipping_rates(s, url_shipping_rates, profile, headers, proxy):
	url = '{}?shipping_address[zip]={}&shipping_address[country]=United States&shipping_address[province]={}'.format(url_shipping_rates, profile.shipping_zip, profile.shipping_state)
	r = s.get(url, headers=headers, proxies=proxy).json()
	shipping_details = {}
	shipping_details['source'] = r['shipping_rates'][0]['source']
	shipping_details['code'] = r['shipping_rates'][0]['code']
	shipping_details['price'] = r['shipping_rates'][0]['price']
	shipping_details['shipping_code'] = urllib.parse.quote('{}-{}-{}'.format(shipping_details['source'], shipping_details['code'], shipping_details['price']), safe='()$')
	return shipping_details

def get_session_id(billing):
	url_payment_gateway_endpoint = 'https://deposit.us.shopifycs.com/sessions'
	card = '{} {} {} {}'.format(billing.card_number[:4], billing.card_number[4:8], billing.card_number[8:12], billing.card_number[12:])

	payload = json.dumps({
		'credit_card': {
			'number': card,
			'name': billing.name_on_card,
			'month': billing.exp_month,
			'year': billing.exp_year,
			'verification_value': billing.cvv
		}
	})
	headers = {
		'accept': 'application/json',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,pt;q=0.6',
		'content-type': 'application/json',
		'host': 'deposit.us.shopifycs.com',
		'origin': 'https://checkout.us.shopifycs.com',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
	}
	r = requests.post(url_payment_gateway_endpoint, headers=headers, data=payload).json()
	session_id = r['id']
	print('    [SESSION ID]: {}'.format(session_id))
	return session_id

def check_shopify_api_key(url):
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
	}
	shopify = {
		'api_key': None,
		'base_url': None,
		'status': 'Failed'
	}
	try:
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.text, 'html.parser')
		element = soup.find('meta', {'name': 'shopify-checkout-api-token'})
		if element:
			token = element['content']
			print(f'[METHOD 1]: {token}')
			shopify['api_key'] = token
			shopify['base_url'] = r.url
			shopify['status'] = 'Success'
			return shopify
		element = soup.find('script', {'id': 'shopify-features'})
		if element:
			data = json.loads(element.get_text())
			token = data['accessToken']
			print(f'[METHOD 2]: {token}')
			shopify['api_key'] = token
			shopify['base_url'] = r.url
			shopify['status'] = 'Success'
			return shopify
	except:
		return shopify

def get_encrypted_card(public_key, card_number, key_id=None, ca=False):
	if ca:
		k = f'-----BEGIN PUBLIC KEY-----\r\n{public_key}\r\n-----END PUBLIC KEY-----\r\n'
		key = RSA.import_key(k)
	else:
		key = RSA.import_key(public_key)
	if ca:
		cipher_rsa = PKCS1_OAEP.new(key)
		last_four = card_number[12:]
		encrypted = cipher_rsa.encrypt(card_number.encode('utf-8'))
		b64_encrypted = base64.b64encode(encrypted).decode('utf-8')
		number = f'{b64_encrypted}{last_four}'
	else:
		cipher_rsa = PKCS1_OAEP.new(key)
		last_four = card_number[12:]
		encrypted = cipher_rsa.encrypt(card_number.encode('utf-8'))
		b64_encrypted = base64.b64encode(encrypted).decode('utf-8')
		bin_number = card_number[:6]
		hidden_card = f'{bin_number}000000{last_four}'
		number = f'{b64_encrypted}:3:{key_id}:{hidden_card}'
	print(number)
	return number

def post_webhook(title, store, link, price, qty, src, color, size):
	url = 'https://discordapp.com/api/webhooks/626625411295739904/c2tST5AbhPPon07yfPCW7e9gYJE-7CgqS-d1Cm5EgaQSl7hiNcc86zR0ebOvDHlKlE_z'
	# url = 'https://discordapp.com/api/webhooks/601232887219748874/tu1D8PBWC7STcVZ0nPArrvKiFoSVApLroINAOHC54a9SUA0XKKrE-DVj5TKw3JEF4_-P'
	t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	payload = {
		'username': 'Success',
		'avatar_url': 'https://i.imgur.com/E6zcSEY.png',
		'embeds': [{
			'title': 'The Gecko App just cooked:',
			'description': f'[{title}]({link})',
			'color': 9946999,
			'thumbnail': {
				'url': f'{src}'
			},
			'fields': [
				{
					'name': 'Store',
					'value': f'[{store}]({store})',
					'inline': True
				},
				{
					'name': 'Price',
					'value': f'{price}',
					'inline': True
				},
				{
					'name': 'Qty',
					'value': f'{qty}',
					'inline': True
				},
				{
					'name': 'Color',
					'value': f'{color}',
					'inline': True
				},
				{
					'name': 'Size',
					'value': f'{size}',
					'inline': True
				}
			],
			'footer': {
				'text': 'Powered by The Gecko App | @jayimshan',
				'icon_url': 'https://i.imgur.com/E6zcSEY.png'
			},
			'timestamp': t
		}]
	}
	requests.post(url, json=payload)

def gen_akamai():
	headers={
	    "accept": "*/*",
	    "accept-encoding": "gzip, deflate, br",
	    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
	    "content-type": "application/json",
	    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
	}
	url = 'https://www.bestbuy.com/'
	s = requests.Session()
	r = s.get(url, headers=headers)
	print(r)
	cookie = None
	for c in r.cookies:
		if 'abck' in c.name:
			print(c.value)
			cookie = c.value

	url = 'https://www.bestbuy.com/resources/b564d4d214196368bcbb9625d68ac8'
	sensor_data_1 = {
		'sensor_data': f'7a74G7m23Vrp0o5c9163791.54-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0,uaend,11059,20100101,en-US,Gecko,0,0,0,0,390770,761395,5120,1410,5120,1440,1709,1330,3083,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:1,sc:0,wrc:1,isc:105,vib:1,bat:0,x11:0,x12:1,5561,0.621120255310,794095380697.5,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,0,0,0,0,1487,231,0;0,-1,0,1,1627,1627,0;-1,2,-94,-102,0,0,0,0,1487,231,0;0,-1,0,1,1627,1627,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.bestbuy.com/-1,2,-94,-115,1,32,32,0,0,0,0,2,0,1588190761395,-999999,16990,0,0,2831,0,0,7,0,0,{cookie},31421,-1,-1,26067385-1,2,-94,-106,0,0-1,2,-94,-119,-1-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,-1-1,2,-94,-80,94-1,2,-94,-116,761402-1,2,-94,-118,77183-1,2,-94,-121,;9;-1;1'
	}

	r = s.post(url, json=sensor_data_1, headers=headers)
	print(r)
	for c in s.cookies:
		if 'abck' in c.name:
			print(c.value)
			cookie = c.value

	sensor_data_2 = {
		'sensor_data': f'7a74G7m23Vrp0o5c9163791.54-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0,uaend,11059,20100101,en-US,Gecko,0,0,0,0,390770,761395,5120,1410,5120,1440,1709,1330,3083,,cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:1,sc:0,wrc:1,isc:105,vib:1,bat:0,x11:0,x12:1,5561,0.746556369373,794095380703.5,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,0,0,0,0,1487,231,0;0,-1,0,1,1627,1627,0;-1,2,-94,-102,0,0,0,0,1487,231,0;0,-1,0,1,1627,1627,0;-1,2,-94,-108,-1,2,-94,-110,-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,-94,-112,https://www.bestbuy.com/-1,2,-94,-115,1,32,32,0,0,0,0,932,0,1588190761407,142,16990,0,0,2831,0,0,934,0,0,{cookie},31911,342,-426645306,26067385-1,2,-94,-106,9,1-1,2,-94,-119,200,0,0,200,200,200,400,200,0,400,0,1000,600,200,-1,2,-94,-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11133333331333333333-1,2,-94,-70,1544133244;-1753895270;dis;;true;true;true;240;true;24;24;true;false;unspecified-1,2,-94,-80,6454-1,2,-94,-116,761402-1,2,-94,-118,81401-1,2,-94,-121,;3;13;0'
	}

	r = s.post(url, json=sensor_data_2, headers=headers)
	print(r)
	jar = {}
	for c in s.cookies:
		if 'abck' in c.name:
			print(c.value)
			jar['name'] = c.name
			jar['value'] = c.value
			jar['domain'] = c.domain

	return jar

# def post_webhook(title, store, link, price, qty, src, color, size):
# 	url_success = 'https://discordapp.com/api/webhooks/626625411295739904/c2tST5AbhPPon07yfPCW7e9gYJE-7CgqS-d1Cm5EgaQSl7hiNcc86zR0ebOvDHlKlE_z'
# 	webhook = DiscordWebhook(url_success)
# 	embed = DiscordEmbed(title='{}'.format(title), color=0x3cd13a)
# 	embed.set_author(name='Success! The Gecko App just cooked:')
# 	embed.add_embed_field(name='Store', value='{}'.format(store))
# 	embed.add_embed_field(name='Price', value='${0:.2f}'.format(price))
# 	embed.add_embed_field(name='Qty', value='{}'.format(qty))
# 	embed.add_embed_field(name='Link', value='{}'.format(link))
# 	embed.add_embed_field(name='Color', value='{}'.format(color))
# 	embed.add_embed_field(name='Size', value='{}'.format(size))
# 	embed.set_thumbnail(url=src)
# 	embed.set_footer(text='Powered by The Gecko App | @jayimshan', icon_url='https://i.imgur.com/E6zcSEY.png')
# 	embed.set_timestamp()
# 	webhook.add_embed(embed)
# 	webhook.execute()

# def post_custom_webhook(url, title, store, link, price, qty, src, color, size):
# 	webhook = DiscordWebhook(url)
# 	embed = DiscordEmbed(title='{}'.format(title), color=0x3cd13a)
# 	embed.set_author(name='Success! The Gecko App just cooked:')
# 	embed.add_embed_field(name='Store', value='{}'.format(store))
# 	embed.add_embed_field(name='Price', value='${0:.2f}'.format(price))
# 	embed.add_embed_field(name='Qty', value='{}'.format(qty))
# 	embed.add_embed_field(name='Link', value='{}'.format(link))
# 	embed.add_embed_field(name='Color', value='{}'.format(color))
# 	embed.add_embed_field(name='Size', value='{}'.format(size))
# 	embed.set_thumbnail(url=src)
# 	embed.set_footer(text='Powered by The Gecko App | @jayimshan', icon_url='https://i.imgur.com/E6zcSEY.png')
# 	embed.set_timestamp()
# 	webhook.add_embed(embed)
# 	webhook.execute()

# def post_monitor_custom_webhook(url, title, store, link, src, status, stock):
# 	webhook = DiscordWebhook(url)
# 	embed = DiscordEmbed(title='{}'.format(title), color=0x3cd13a)
# 	embed.set_author(name='Success! The Gecko App just cooked:')
# 	embed.add_embed_field(name='Store', value='{}'.format(store))
# 	embed.add_embed_field(name='Status', value='{}'.format(status))
# 	embed.add_embed_field(name='Stock', value='{}'.format(stock))
# 	embed.add_embed_field(name='Link', value='{}'.format(link))
# 	embed.set_thumbnail(url=src)
# 	embed.set_footer(text='Powered by The Gecko App | @jayimshan', icon_url='https://i.imgur.com/E6zcSEY.png')
# 	embed.set_timestamp()
# 	webhook.add_embed(embed)
# 	webhook.execute()