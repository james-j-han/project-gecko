from bs4 import BeautifulSoup

import requests
import json
import time

# headers = {
# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 	'Accept-Encoding': 'gzip, deflate, br',
# 	'Accept-Language': 'en-US,en;q=0.5',
# 	'Host': 'www.walmart.com',
# 	'Upgrade-Insecure-Requests': '1',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
# }

# url = 'https://www.walmart.com/ip/2017-Panini-NFL-Donruss-Exclusive-Hanger-Box/417996847'

# r = requests.get(url, headers=headers)
# print(r)
# soup = BeautifulSoup(r.text, 'lxml')
# item = soup.find('script', {'id': 'item'}).contents[0]
# data = json.loads(item)
# print(data)
# offer_ID = data['item']['product']['buyBox']['products'][0]['offerId']
# print(offer_ID)

# print(int(time.time()))

# pie = '''
# // PIE version: 1.2.1

# var PIE = {};  // PIE namespace

# // dynamically-generated PIE settings
# PIE.L = 6;
# PIE.E = 4;
# PIE.K = "23EA4FEBA3140EB4DEE44328C178C34E";
# PIE.key_id = "b2c8e976";
# PIE.phase = 1;
# '''

# PIE_L = int(pie.split('PIE.L = ')[1].split(';')[0])
# PIE_E = int(pie.split('PIE.E = ')[1].split(';')[0])
# PIE_K = pie.split('PIE.K = "')[1].split('";')[0]
# PIE_key_ID = pie.split('PIE.key_id = "')[1].split('";')[0]
# PIE_phase = int(pie.split('PIE.phase = ')[1].split(';')[0])
# print(PIE_L)
# print(PIE_E)
# print(PIE_K)
# print(PIE_key_ID)
# print(PIE_phase)

tcin = 79503655
# url = 'https://carts.target.com/web_checkouts/v1/cart_items'
url = f'https://redsky.target.com/v3/pdp/tcin/{tcin}'
headers = {
	'content-type': 'application/json',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
	'x-application-name': 'web'
}
params = {
	'excludes': 'taxonomy,bulk_ship,awesome_shop,question_answer_statistics,rating_and_review_reviews,rating_and_review_statistics,deep_red_labels,in_store_location',
	'key': 'eb2551e4accc14f38cc42d32fbc2b2ea'
}
r = requests.get(url, headers=headers, params=params)
print(r)
data = r.json()
print(data)