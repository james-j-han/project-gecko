import queue
import random
import threading

# VERSION 1.1
class Proxy:

	def __init__(self, proxy_id, proxy_name, proxies):
		self.proxy_id = proxy_id
		self.proxy_name = proxy_name
		self.proxies = proxies

		self.proxy_list = []
		self.seq_pool = queue.Queue()
		self.ran_pool = queue.Queue()

		self.split_proxies()
		self.create_seq_pool()
		self.create_ran_pool()

		self.lock = threading.Lock()

	def split_proxies(self):
		for proxy in self.proxies.split('\n'):
			self.proxy_list.append(self.sort_proxy(proxy))

	def sort_proxy(self, proxy):
		parts = proxy.split(':')
		if len(parts) == 4:
			sorted_proxy = {'https': f'https://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}'}
		else:
			sorted_proxy = {'http': f'http://{parts[0]}:{parts[1]}'}

		return sorted_proxy

	def create_ran_pool(self):
		pl = self.proxy_list
		random.shuffle(pl)
		for proxy in pl:
			self.ran_pool.put(proxy)

	def create_seq_pool(self):
		pl = self.proxy_list
		for proxy in pl:
			self.seq_pool.put(proxy)

	def get_proxy(self, proxy, rotation):
		if proxy:
			with self.lock:
				if rotation == 'Sequential':
					self.seq_pool.put(proxy)
					p = self.seq_pool.get()
				else:
					self.ran_pool.put(proxy)
					p = self.ran_pool.get()
		else:
			with self.lock:
				if rotation == 'Sequential':
					p = self.seq_pool.get()
				else:
					p = self.ran_pool.get()
		
		return p