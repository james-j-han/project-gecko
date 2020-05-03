import queue
import random
import threading

class Proxy:

	def __init__(self, proxy_id=None, proxy_name='localhost', proxies=None):
		self.proxy_id = proxy_id
		self.proxy_name = proxy_name
		self.proxies = proxies
		self.proxy_list = self.split_proxies()
		# self.pool = queue.Queue()

		self.seq_pool = self.get_seq_queue()
		self.ran_pool = self.get_ran_queue()
		self.lock = threading.Lock()

	def split_proxies(self):
		proxy_list = []
		if self.proxies:
			for proxy in self.proxies.split('\n'):
				parts = proxy.split(':')
				combined = {'https': 'https://{}:{}@{}:{}'.format(parts[2], parts[3], parts[0], parts[1])}
				proxy_list.append(combined)
				# self.pool.put(combined)
		return proxy_list

	def get_ran_queue(self):
		q = queue.Queue()
		random.shuffle(self.proxy_list)
		for proxy in self.proxy_list:
			q.put(proxy)
		return q
		# self.set_queue(self.proxy_list)

	def get_seq_queue(self):
		# self.proxy_list = self.split_proxies()
		# self.set_queue(self.proxy_list)
		q = queue.Queue()
		for proxy in self.proxy_list:
			q.put(proxy)
		return q

	def get_ran_proxy(self):
		proxy = None
		with self.lock:
			print('GET Lock aquired')
			proxy = self.ran_pool.get()
			print('GET Lock release')
		return proxy

	def get_seq_proxy(self):
		proxy = None
		with self.lock:
			print('GET Lock aquired')
			proxy = self.seq_pool.get()
			print('GET Lock release')
		return proxy

	def put_ran_proxy(self, proxy):
		with self.lock:
			print('PUT Lock aquired')
			self.ran_pool.put(proxy)
			print('PUT Lock release')

	def put_seq_proxy(self, proxy):
		with self.lock:
			print('PUT Lock aquired')
			self.seq_pool.put(proxy)
			print('PUT Lock release')

	# def set_queue(self, proxy_list):
	# 	self.pool.queue.clear()
	# 	for proxy in proxy_list:
	# 		self.pool.put(proxy)

	# def get_queue_random(self):
	# 	proxies = self.proxy_list


	# def get_proxy(self):
	# 	proxy = self.pool.get()
	# 	self.pool.put(proxy)
	# 	return proxy