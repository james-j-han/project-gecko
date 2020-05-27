# CLIENT ID 712386522221117440
# TOKEN NzEyMzg2NTIyMjIxMTE3NDQw.XsQzwA.l5BLZubhhG4VIN7Nj1spiPzje6Y
# PERM 67584

# url = 'https://discordapp.com/oauth2/authorize?client_id=712386522221117440&scope=bot&permissions=67584'

from bs4 import BeautifulSoup
from discord.ext import commands

import discord
import requests
import datetime

token = 'NzEyMzg2NTIyMjIxMTE3NDQw.XsQzwA.l5BLZubhhG4VIN7Nj1spiPzje6Y'
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
	# print(f'We have logged in as {client.user}')
	print('Bot is ready')

@client.command()
async def ebayprice(ctx, *args):
	search = ''
	for kw in args:
		search += f'{kw} '

	url = 'https://www.ebay.com/sch/i.html'
	params = {
		'_nkw': search,
		'LH_Sold': '1',
		'LH_Complete': '1',
		'_ipg': '100'
	}

	r = requests.get(url, params=params)
	soup = BeautifulSoup(r.text, 'lxml')
	items = soup.find_all('div', {'class': 's-item__details'})

	count = 0
	free_shipping_count = 0
	charge_shipping_count = 0
	total_sold_amount = 0.00
	total_shipping = 0.00

	for item in items:
		span_price = item.find('span', {'class': 's-item__price'}).find('span', {'class': 'POSITIVE'})
		span_shipping = item.find('span', {'class': 's-item__shipping'})
		
		if len(span_price['class']) == 1:
			total_sold_amount += float(span_price.text.strip().split('$')[-1])
			count += 1	

		if 'free' in span_shipping.text.strip().lower():
			free_shipping_count += 1
		else:
			total_shipping += float(span_shipping.text.strip().split(' ')[0].split('$')[-1])
			charge_shipping_count += 1

	average_sold_price = f'${total_sold_amount/count:.2f}'
	average_shipping = f'${total_shipping/charge_shipping_count:.2f}'

	embed = discord.Embed(
		# title='eBay Price Check',
		avatar_url='https://i.imgur.com/6pY05I4.jpg',
		description=f'[{count}/100 results for: {search}]({r.url})',
		colour=9946999,
		timestamp=datetime.datetime.utcnow()
	)
	embed.set_author(
		name='eBay Price & Shipping',
		icon_url='https://i.imgur.com/TwRP6Dw.png'
	)
	embed.add_field(name='Average Sold Price', value=f'{average_sold_price}', inline=True)
	embed.add_field(name='Average Shipping', value=f'{average_shipping}', inline=True)
	embed.add_field(name='Free Shipping', value=f'{free_shipping_count}/100 offered free shipping', inline=True)
	embed.set_footer(
		text='Powered by The Gecko App | @jayimshan',
		icon_url='https://i.imgur.com/E6zcSEY.png'
	)
	await ctx.send(embed=embed)

def post_webhook():
	url = 'https://discordapp.com/api/webhooks/601232887219748874/tu1D8PBWC7STcVZ0nPArrvKiFoSVApLroINAOHC54a9SUA0XKKrE-DVj5TKw3JEF4_-P'
	t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	payload = {
		'username': 'Gecko',
		'embeds': [{
			'title': 'Testing',
			'timestamp': t
		}]
	}
	requests.post(url, json=payload)

# def post_webhook(title, store, link, price, src):
# 	url = 'https://discordapp.com/api/webhooks/711733171355385927/Nryrw-4uocr54U_esXV1z7SLC2l6Dv1oNky-eV8LDcAimr8cDfmifIiOQRjCOekvIFY3'
# 	t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
# 	payload = {
# 		'username': 'Restock',
# 		# 'avatar_url': 'https://i.imgur.com/zhZUSyh.jpg',
# 		'embeds': [{
# 			'author': {
# 				'name': 'Disney',
# 				'icon_url': 'https://i.imgur.com/oFpjIAx.jpg'
# 			},
# 			# 'title': f'Disney',
# 			'description': f'[{title}]({link})',
# 			'color': 9946999,
# 			'thumbnail': {
# 				'url': f'{src}'
# 			},
# 			'fields': [
# 				{
# 					'name': 'Status',
# 					'value': 'In Stock',
# 					'inline': True
# 				},
# 				{
# 					'name': 'Price',
# 					'value': f'{price}',
# 					'inline': True
# 				}
# 			],
# 			'footer': {
# 				'text': 'Powered by The Gecko App | @jayimshan',
# 				'icon_url': 'https://i.imgur.com/E6zcSEY.png'
# 			},
# 			'timestamp': t
# 		}]
# 	}
# 	requests.post(url, json=payload)

try:
	client.run(token)
except KeyboardInterrupt:
	client.close()