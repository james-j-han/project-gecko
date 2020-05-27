from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtNetwork

from bs4 import BeautifulSoup

import requests
import discord
import asyncio
import json
import time

import gecko_utils

# VERSION 0.1
class Ebay(QObject):

	update_title = pyqtSignal()
	update_image = pyqtSignal()
	update_size = pyqtSignal()
	update_status = pyqtSignal()
	
	request_captcha = pyqtSignal()
	poll_response = pyqtSignal()

	channel_ID = '601229394572476427'

	def __init__(self, task_type, search, qty, size, color, profile, billing):
		super().__init__()
		self.s = requests.Session()
		self.client = discord.Client()
		self.on_ready = self.client.event(self.on_ready)
		self.on_message = self.client.event(self.on_message)
		self.on_disconnect = self.client.event(self.on_disconnect)

		# self.loop = asyncio.get_event_loop()
		# self.loop.create_task(self.run_2())
		# asyncio.set_event_loop(self.loop)

		self.task_type = task_type
		self.search = search
		self.profile = profile
		self.billing = billing

        # Webhook info
		self.store = 'https://www.ebay.com/'
		self.title = None
		self.src = None
		self.link = None
		self.price = None
		self.qty = qty
		self.color = color
		self.size = size
		
		self.status = 'Ready'
		self.abort = False
		self.current_step = 0
		self.steps = [
			self.run
		]

	async def on_ready(self):
		print(f'Logged in as {self.client.user}')
		self.status = f'Logged in as {self.client.user}'
		self.update_status.emit()

	async def on_message(self, message):
		print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')

		if 'shutdown' in message.content:
			await self.client.close()

	async def on_disconnect(self):
		print(f'{self.client.user} logged out')
		self.status = f'{self.client.user} logged out'
		self.update_status.emit()

	def run(self):
		try:
			self.client.loop.run_until_complete(self.run_2())
		except KeyboardInterrupt:
			pass
			# self.client.loop.run_until_complete(self.logout())
		finally:
			self.client.loop.close()
		# self.client.run('NzEyMzg2NTIyMjIxMTE3NDQw.XsQzwA.l5BLZubhhG4VIN7Nj1spiPzje6Y')

	async def run_2(self):
		# await self.client.wait_until_ready()
		await self.client.start('NzEyMzg2NTIyMjIxMTE3NDQw.XsQzwA.l5BLZubhhG4VIN7Nj1spiPzje6Y')

		# while not self.abort:
		# 	print('Looping')
		# 	await asyncio.sleep(1)

		# await self.client.loop.close()


	def logout(self):
		print('Logging out')
		# self.abort = True
		# self.client.loop.stop()