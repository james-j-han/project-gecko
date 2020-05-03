import sqlite3

class TheGeckoAppDatabase():

	def __init__(self, database):
		self.con = sqlite3.connect('{}'.format(database))
		self.cur = self.con.cursor()
		self.cur.execute("PRAGMA foreign_keys=ON")

	def create_table_keys(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS keys (
					id INTEGER PRIMARY KEY,
					key TEXT
				)
				""")

	def create_table_tasks(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS tasks (
					id INTEGER PRIMARY KEY,
					line_edit_task_name TEXT,
					combo_box_task_type TEXT,
					combo_box_store TEXT,
					combo_box_qty INTEGER,
					check_box_captcha INTEGER,
					combo_box_search_type TEXT,
					line_edit_search TEXT,
					check_box_account INTEGER,
					combo_box_accounts INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
					combo_box_profiles INTEGER REFERENCES profiles(id) ON DELETE CASCADE,
					combo_box_billing INTEGER REFERENCES billing(id) ON DELETE CASCADE,
					check_box_proxies INTEGER,
					combo_box_proxies INTEGER REFERENCES proxies(id) ON DELETE CASCADE,
					combo_box_rotation TEXT,
					check_box_category INTEGER,
					combo_box_category TEXT,
					check_box_size INTEGER,
					combo_box_size TEXT,
					check_box_color INTEGER,
					line_edit_color TEXT,
					line_edit_retry_delay TEXT,
					check_box_retry_variance INTEGER,
					line_edit_retry_variance TEXT,
					check_box_checkout_delay INTEGER,
					line_edit_checkout_delay TEXT,
					check_box_checkout_variance INTEGER,
					line_edit_checkout_variance TEXT,
					base_url TEXT,
					api_key TEXT
				)
				""")

	def create_table_profiles(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS profiles (
					id INTEGER PRIMARY KEY,
					profile_name TEXT,
					first_name TEXT,
					last_name TEXT,
					email TEXT,
					phone TEXT,
					check_box_same_as_shipping INTEGER,
					shipping_address TEXT,
					shipping_address_2 TEXT,
					shipping_city TEXT,
					shipping_state TEXT,
					shipping_zip TEXT,
					billing_address TEXT,
					billing_address_2 TEXT,
					billing_city TEXT,
					billing_state TEXT,
					billing_zip TEXT
				)
				""")

	def create_table_billing(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS billing (
					id INTEGER PRIMARY KEY,
					billing_name TEXT,
					name_on_card TEXT,
					card_type TEXT,
					card_number TEXT,
					exp_month TEXT,
					exp_year TEXT,
					cvv TEXT
				)
				""")

	def create_table_proxies(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS proxies (
					id INTEGER PRIMARY KEY,
					proxy_name TEXT,
					proxies TEXT
				)
				""")

	def create_table_accounts(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS accounts (
					id INTEGER PRIMARY KEY,
					account_name TEXT,
					account_store TEXT,
					account_cookies TEXT
				)
				""")

	def create_table_settings(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS settings (
					id INTEGER PRIMARY KEY,
				)
				""")

	def update_task(self, key, value, task_id):
		with self.con:
			self.cur.execute("UPDATE tasks SET {}=? WHERE id={}".format(key, task_id), (value,))

	def save_task(self, items, task_id=None):
		with self.con:
			if task_id:
				self.cur.execute("""UPDATE tasks SET 
					line_edit_task_name=?,
					combo_box_task_type=?,
					combo_box_store=?,
					combo_box_qty=?,
					check_box_captcha=?,
					combo_box_search_type=?,
					line_edit_search=?,
					check_box_account=?,
					combo_box_accounts=?,
					combo_box_profiles=?,
					combo_box_billing=?,
					check_box_proxies=?,
					combo_box_proxies=?,
					combo_box_rotation=?,
					check_box_category=?,
					combo_box_category=?,
					check_box_size=?,
					combo_box_size=?,
					check_box_color=?,
					line_edit_color=?,
					line_edit_retry_delay=?,
					check_box_retry_variance=?,
					line_edit_retry_variance=?,
					check_box_checkout_delay=?,
					line_edit_checkout_delay=?,
					check_box_checkout_variance=?,
					line_edit_checkout_variance=?,
					base_url=?,
					api_key=?
					WHERE id={}""".format(task_id), (
						items['line_edit_task_name'],
						items['combo_box_task_type'],
						items['combo_box_store'],
						items['combo_box_qty'],
						items['check_box_captcha'],
						items['combo_box_search_type'],
						items['line_edit_search'],
						items['check_box_account'],
						items['combo_box_accounts'],
						items['combo_box_profiles'],
						items['combo_box_billing'],
						items['check_box_proxies'],
						items['combo_box_proxies'],
						items['combo_box_rotation'],
						items['check_box_category'],
						items['combo_box_category'],
						items['check_box_size'],
						items['combo_box_size'],
						items['check_box_color'],
						items['line_edit_color'],
						items['line_edit_retry_delay'],
						items['check_box_retry_variance'],
						items['line_edit_retry_variance'],
						items['check_box_checkout_delay'],
						items['line_edit_checkout_delay'],
						items['check_box_checkout_variance'],
						items['line_edit_checkout_variance'],
						items['base_url'],
						items['api_key']
						))
			else:
				self.cur.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
					task_id,
					items['line_edit_task_name'],
					items['combo_box_task_type'],
					items['combo_box_store'],
					items['combo_box_qty'],
					items['check_box_captcha'],
					items['combo_box_search_type'],
					items['line_edit_search'],
					items['check_box_account'],
					items['combo_box_accounts'],
					items['combo_box_profiles'],
					items['combo_box_billing'],
					items['check_box_proxies'],
					items['combo_box_proxies'],
					items['combo_box_rotation'],
					items['check_box_category'],
					items['combo_box_category'],
					items['check_box_size'],
					items['combo_box_size'],
					items['check_box_color'],
					items['line_edit_color'],
					items['line_edit_retry_delay'],
					items['check_box_retry_variance'],
					items['line_edit_retry_variance'],
					items['check_box_checkout_delay'],
					items['line_edit_checkout_delay'],
					items['check_box_checkout_variance'],
					items['line_edit_checkout_variance'],
					items['base_url'],
					items['api_key']
					))

	def save_profile(self, items, profile_id=None):
		with self.con:
			if profile_id:
				self.cur.execute("""UPDATE profiles SET
					profile_name=?,
					first_name=?,
					last_name=?,
					email=?,
					phone=?,
					check_box_same_as_shipping=?,
					shipping_address=?,
					shipping_address_2=?,
					shipping_city=?,
					shipping_state=?,
					shipping_zip=?,
					billing_address=?,
					billing_address_2=?,
					billing_city=?,
					billing_state=?,
					billing_zip=?
					WHERE id={}""".format(profile_id), (
						items['profile_name'],
						items['first_name'],
						items['last_name'],
						items['email'],
						items['phone'],
						items['same_as_shipping'],
						items['shipping_address'],
						items['shipping_address_2'],
						items['shipping_city'],
						items['shipping_state'],
						items['shipping_zip'],
						items['billing_address'],
						items['billing_address_2'],
						items['billing_city'],
						items['billing_state'],
						items['billing_zip']
						))
			else:
				self.cur.execute("INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
					profile_id,
					items['profile_name'],
					items['first_name'],
					items['last_name'],
					items['email'],
					items['phone'],
					items['same_as_shipping'],
					items['shipping_address'],
					items['shipping_address_2'],
					items['shipping_city'],
					items['shipping_state'],
					items['shipping_zip'],
					items['billing_address'],
					items['billing_address_2'],
					items['billing_city'],
					items['billing_state'],
					items['billing_zip']
					))

	def save_billing(self, items, billing_id=None):
		with self.con:
			if billing_id:
				self.cur.execute("""UPDATE billing SET
					billing_name=?,
					name_on_card=?,
					card_type=?,
					card_number=?,
					exp_month=?,
					exp_year=?,
					cvv=?
					WHERE id={}""".format(billing_id), (
						items['billing_name'],
						items['name_on_card'],
						items['card_type'],
						items['card_number'],
						items['exp_month'],
						items['exp_year'],
						items['cvv']
						))
			else:
				self.cur.execute("INSERT INTO billing VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
					billing_id,
					items['billing_name'],
					items['name_on_card'],
					items['card_type'],
					items['card_number'],
					items['exp_month'],
					items['exp_year'],
					items['cvv']
					))

	def save_proxy(self, items, proxy_id=None):
		with self.con:
			if proxy_id:
				self.cur.execute("""UPDATE proxies SET
					proxy_name=?,
					proxies=?
					WHERE id={}""".format(proxy_id), (
						items['proxy_name'],
						items['proxies']
						))
			else:
				self.cur.execute("INSERT INTO proxies VALUES (?, ?, ?)", (
					proxy_id,
					items['proxy_name'],
					items['proxies']
					))

	def update_account(self, key, value, account_id):
		with self.con:
			self.cur.execute("UPDATE accounts SET {}=? WHERE id={}".format(key, account_id), (value,))

	def save_account(self, items, account_id=None):
		with self.con:
			if account_id:
				self.cur.execute("""UPDATE accounts SET
					account_name=?,
					account_store=?,
					account_cookies=?
					WHERE id={}""".format(account_id), (
						items['account_name'],
						items['account_store'],
						items['account_cookies']
						))
			else:
				self.cur.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (
					account_id,
					items['account_name'],
					items['account_store'],
					items['account_cookies']
					))

	def save_key(self, key, key_id=None):
		with self.con:
			if key_id:
				self.cur.execute("""UPDATE keys SET
					key=?
					WHERE id={}""".format(key_id), (
						key,
					))
			else:
				self.cur.execute("INSERT INTO keys VALUES (?, ?)", (
					key_id,
					key
					))

	def delete_task(self, task_id):
		with self.con:
			self.cur.execute("DELETE FROM tasks WHERE id={}".format(task_id))

	def delete_all_tasks(self):
		with self.con:
			self.cur.execute("DELETE FROM tasks")

	def delete_profile(self, profile_id):
		with self.con:
			self.cur.execute("DELETE FROM profiles WHERE id={}".format(profile_id))

	def delete_all_profiles(self):
		with self.con:
			self.cur.execute("DELETE FROM profiles")

	def delete_billing(self, billing_id):
		with self.con:
			self.cur.execute("DELETE FROM billing WHERE id={}".format(billing_id))

	def delete_all_billing(self):
		with self.con:
			self.cur.execute("DELETE FROM billing")

	def delete_proxy(self, proxy_id):
		with self.con:
			self.cur.execute("DELETE FROM proxies WHERE id={}".format(proxy_id))

	def delete_all_proxies(self):
		with self.con:
			self.cur.execute("DELETE FROM proxies")

	def delete_account(self, account_id):
		with self.con:
			self.cur.execute("DELETE FROM accounts WHERE id={}".format(account_id))

	def delete_all_accounts(self):
		with self.con:
			self.cur.execute("DELETE FROM accounts")

	def get_all_billing(self):
		with self.con:
			self.cur.execute("SELECT * FROM billing")
		return self.cur.fetchall()

	def get_billing(self, billing_id):
		with self.con:
			self.cur.execute("SELECT * FROM billing WHERE id={}".format(billing_id))
		return self.cur.fetchall()

	def get_all_profiles(self):
		with self.con:
			self.cur.execute("SELECT * FROM profiles")
		return self.cur.fetchall()

	def get_profile(self, profile_id):
		with self.con:
			self.cur.execute("SELECT * FROM profiles WHERE id={}".format(profile_id))
		return self.cur.fetchall()

	def get_all_proxies(self):
		with self.con:
			self.cur.execute("SELECT * FROM proxies")
		return self.cur.fetchall()

	def get_proxy(self, proxy_id):
		with self.con:
			self.cur.execute("SELECT * FROM proxies WHERE id={}".format(proxy_id))
		return self.cur.fetchall()

	def get_all_tasks(self):
		with self.con:
			self.cur.execute("SELECT * FROM tasks")
		return self.cur.fetchall()

	def get_task(self, task_id):
		with self.con:
			self.cur.execute("SELECT * FROM tasks WHERE id={}".format(task_id))
		return self.cur.fetchall()

	def get_recent_task(self):
		with self.con:
			self.cur.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")
		return self.cur.fetchall()

	def get_all_accounts(self):
		with self.con:
			self.cur.execute("SELECT * FROM accounts")
		return self.cur.fetchall()

	def get_account(self, account_id):
		with self.con:
			self.cur.execute("SELECT * FROM accounts WHERE id={}".format(account_id))
		return self.cur.fetchall()

	def get_recent_account(self):
		with self.con:
			self.cur.execute("SELECT * FROM accounts ORDER BY id DESC LIMIT 1")
		return self.cur.fetchall()

	def get_key(self):
		with self.con:
			self.cur.execute("SELECT * FROM keys WHERE id=1")
		return self.cur.fetchall()