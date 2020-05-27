from bs4 import BeautifulSoup
from urllib.request import urlopen

import requests
import datetime
import json
import time
import os

# headers = {
# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 	'Accept-Encoding': 'gzip, deflate, br',
# 	'Accept-Language': 'en-US,en;q=0.5',
# 	'Host': 'www.ebay.com',
# 	'Upgrade-Insecure-Requests': '1',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
# }

# url = 'https://www.ebay.com/sch/i.html'
# search = 'pokemon mystery box 7'

# params = {
# 	'_nkw': search,
# 	'LH_Sold': '1',
# 	'LH_Complete': '1',
# 	'_ipg': '200'
# }

# r = requests.get(url, headers=headers, params=params)
# print(r)
# soup = BeautifulSoup(r.text, 'html.parser')
# with open('pokemon.html', 'w', encoding='utf-8') as f:
# 	f.write(soup.prettify())

folder = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(folder, 'pokemon.html')
with open(file, 'r', encoding='utf-8') as f:
	data = f.read()

soup = BeautifulSoup(data, 'lxml')
ul = soup.find('ul', {'class': 'srp-results'}).find_all('li', {'class': 's-item'})

count = 0
free_shipping_count = 0
charge_shipping_count = 0
local_pickup_count = 0
total_sold_amount = 0.00
total_shipping = 0.00
recent_sale_link = None
recent_sale_date = ''
recent_sale_amount = ''

try:
	neg = []
	for li in ul:
		item = li.find('a', {'class': 's-item__link'})
		link = item['href']
		title = item.text.strip().lower()
		
		if neg:
			search_type = 'Keyword'
			if any(kw in title for kw in neg):
				print('Negative KW found, continuing...')
				continue
			
		span_price = li.find('span', {'class': 's-item__price'}).find('span', {'class': 'POSITIVE'})
		
		if len(span_price['class']) == 1:
			# Run once for most recent sale/transaction
			if recent_sale_link is None:
				recent_sale_date = li.find('span', {'class': 's-item__ended-date'}).text.strip()
				recent_sale_link = link
				recent_sale_amount = span_price.text.strip()

			char_to_remove = '$,+'
			sale_amount = span_price.text.strip()
			for char in char_to_remove:
				sale_amount = sale_amount.replace(char, '')

			total_sold_amount += float(sale_amount)
			count += 1

			span_shipping = li.find('span', {'class': 's-item__shipping'})
			if span_shipping:
				if 'free' in span_shipping.text.strip().lower():
					free_shipping_count += 1
				elif 'not specified' in span_shipping.text.strip().lower():
					continue
				else:
					print(span_shipping.text.strip())
					shipping_amount = span_shipping.text.strip().split(' ')[0]
					for char in char_to_remove:
						shipping_amount = shipping_amount.replace(char, '')

					total_shipping += float(shipping_amount)
					charge_shipping_count += 1
			else:
				local_pickup_count += 1

	average_sold_price = f'${total_sold_amount/count:.2f}'
	if charge_shipping_count > 0:
		average_shipping = f'${total_shipping/charge_shipping_count:.2f}'
	else:
		average_shipping = f'Free'
	print(average_sold_price)
	print(average_shipping)
except Exception as e:
	print(f'{e}')