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
					combo_box_task_type TEXT,
					combo_box_store TEXT,
					line_edit_custom_shopify TEXT,
					combo_box_search_type TEXT,
					line_edit_search TEXT,
					line_edit_task_name TEXT,
					combo_box_qty INTEGER,
					check_box_account INTEGER,
					combo_box_account INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
					combo_box_profile INTEGER REFERENCES profiles(id) ON DELETE CASCADE,
					combo_box_billing INTEGER REFERENCES billing(id) ON DELETE CASCADE,
					check_box_proxies INTEGER,
					combo_box_proxies INTEGER REFERENCES proxies(id) ON DELETE CASCADE,
					combo_box_rotation TEXT,
					check_box_size INTEGER,
					combo_box_size TEXT,
					check_box_color INTEGER,
					line_edit_color TEXT,
					check_box_category INTEGER,
					combo_box_category TEXT,
					check_box_price_range INTEGER,
					line_edit_price_min TEXT,
					line_edit_price_max TEXT,
					line_edit_delay_min TEXT,
					line_edit_delay_max TEXT,
					check_box_captcha INTEGER
				)
				""")

	def create_table_profiles(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS profiles (
					id INTEGER PRIMARY KEY,
					profile_name TEXT,
					check_box_email_jig INTEGER,
					email TEXT,
					phone TEXT,
					s_first_name TEXT,
					s_last_name TEXT,
					s_address_1 TEXT,
					s_address_2 TEXT,
					s_city TEXT,
					s_state TEXT,
					s_zip TEXT,
					group_box_same_as_shipping INTEGER,
					b_first_name TEXT,
					b_last_name TEXT,
					b_address_1 TEXT,
					b_address_2 TEXT,
					b_city TEXT,
					b_state TEXT,
					b_zip TEXT
				)
				""")

	def create_table_billing(self):
		with self.con:
			self.cur.execute("""
				CREATE TABLE IF NOT EXISTS billing (
					id INTEGER PRIMARY KEY,
					billing_name TEXT,
					card_name TEXT,
					card_number TEXT,
					card_month TEXT,
					card_year TEXT,
					card_cvv TEXT
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
			self.cur.execute(f"UPDATE tasks SET {key}=? WHERE id={task_id}", (value,))

	def save_task(self, items, task_id=None):
		with self.con:
			if task_id:
				self.cur.execute("""UPDATE tasks SET 
					combo_box_task_type=?,
					combo_box_store=?,
					line_edit_custom_shopify=?,
					combo_box_search_type=?,
					line_edit_search=?,
					line_edit_task_name=?,
					combo_box_qty=?,
					check_box_account=?,
					combo_box_account=?,
					combo_box_profile=?,
					combo_box_billing=?,
					check_box_proxies=?,
					combo_box_proxies=?,
					combo_box_rotation=?,
					check_box_size=?,
					combo_box_size=?,
					check_box_color=?,
					line_edit_color=?,
					check_box_category=?,
					combo_box_category=?,
					check_box_price_range=?,
					line_edit_price_min=?,
					line_edit_price_max=?,
					line_edit_delay_min=?,
					line_edit_delay_max=?,
					check_box_captcha=?
					WHERE id={}""".format(task_id), (
						items['combo_box_task_type'],
						items['combo_box_store'],
						items['line_edit_custom_shopify'],
						items['combo_box_search_type'],
						items['line_edit_search'],
						items['line_edit_task_name'],
						items['combo_box_qty'],
						items['check_box_account'],
						items['combo_box_account'],
						items['combo_box_profile'],
						items['combo_box_billing'],
						items['check_box_proxies'],
						items['combo_box_proxies'],
						items['combo_box_rotation'],
						items['check_box_size'],
						items['combo_box_size'],
						items['check_box_color'],
						items['line_edit_color'],
						items['check_box_category'],
						items['combo_box_category'],
						items['check_box_price_range'],
						items['line_edit_price_min'],
						items['line_edit_price_max'],
						items['line_edit_delay_min'],
						items['line_edit_delay_max'],
						items['check_box_captcha']
						))
			else:
				self.cur.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
					task_id,
					items['combo_box_task_type'],
					items['combo_box_store'],
					items['line_edit_custom_shopify'],
					items['combo_box_search_type'],
					items['line_edit_search'],
					items['line_edit_task_name'],
					items['combo_box_qty'],
					items['check_box_account'],
					items['combo_box_account'],
					items['combo_box_profile'],
					items['combo_box_billing'],
					items['check_box_proxies'],
					items['combo_box_proxies'],
					items['combo_box_rotation'],
					items['check_box_size'],
					items['combo_box_size'],
					items['check_box_color'],
					items['line_edit_color'],
					items['check_box_category'],
					items['combo_box_category'],
					items['check_box_price_range'],
					items['line_edit_price_min'],
					items['line_edit_price_max'],
					items['line_edit_delay_min'],
					items['line_edit_delay_max'],
					items['check_box_captcha']
					))

	def save_profile(self, items, profile_id=None):
		with self.con:
			if profile_id:
				self.cur.execute("""UPDATE profiles SET
					profile_name=?,
					check_box_email_jig=?,
					email=?,
					phone=?,
					s_first_name=?,
					s_last_name=?,
					s_address_1=?,
					s_address_2=?,
					s_city=?,
					s_state=?,
					s_zip=?,
					group_box_same_as_shipping=?,
					b_first_name=?,
					b_last_name=?,
					b_address_1=?,
					b_address_2=?,
					b_city=?,
					b_state=?,
					b_zip=?
					WHERE id={}""".format(profile_id), (
						items['profile_name'],
						items['check_box_email_jig'],
						items['email'],
						items['phone'],
						items['s_first_name'],
						items['s_last_name'],
						items['s_address_1'],
						items['s_address_2'],
						items['s_city'],
						items['s_state'],
						items['s_zip'],
						items['group_box_same_as_shipping'],
						items['b_first_name'],
						items['b_last_name'],
						items['b_address_1'],
						items['b_address_2'],
						items['b_city'],
						items['b_state'],
						items['b_zip']
						))
			else:
				self.cur.execute("INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
					profile_id,
					items['profile_name'],
					items['check_box_email_jig'],
					items['email'],
					items['phone'],
					items['s_first_name'],
					items['s_last_name'],
					items['s_address_1'],
					items['s_address_2'],
					items['s_city'],
					items['s_state'],
					items['s_zip'],
					items['group_box_same_as_shipping'],
					items['b_first_name'],
					items['b_last_name'],
					items['b_address_1'],
					items['b_address_2'],
					items['b_city'],
					items['b_state'],
					items['b_zip']
					))

	def save_billing(self, items, billing_id=None):
		with self.con:
			if billing_id:
				self.cur.execute("""UPDATE billing SET
					billing_name=?,
					card_name=?,
					card_number=?,
					card_month=?,
					card_year=?,
					card_cvv=?
					WHERE id={}""".format(billing_id), (
						items['billing_name'],
						items['card_name'],
						items['card_number'],
						items['card_month'],
						items['card_year'],
						items['card_cvv']
						))
			else:
				self.cur.execute("INSERT INTO billing VALUES (?, ?, ?, ?, ?, ?, ?)", (
					billing_id,
					items['billing_name'],
					items['card_name'],
					items['card_number'],
					items['card_month'],
					items['card_year'],
					items['card_cvv']
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

	def get_recent_billing(self):
		with self.con:
			self.cur.execute("SELECT * FROM billing ORDER BY id DESC LIMIT 1")
		return self.cur.fetchall()

	def get_all_profiles(self):
		with self.con:
			self.cur.execute("SELECT * FROM profiles")
		return self.cur.fetchall()

	def get_profile(self, profile_id):
		with self.con:
			self.cur.execute("SELECT * FROM profiles WHERE id={}".format(profile_id))
		return self.cur.fetchall()

	def get_recent_profile(self):
		with self.con:
			self.cur.execute("SELECT * FROM profiles ORDER BY id DESC LIMIT 1")
		return self.cur.fetchall()

	def get_all_proxies(self):
		with self.con:
			self.cur.execute("SELECT * FROM proxies")
		return self.cur.fetchall()

	def get_proxy(self, proxy_id):
		with self.con:
			self.cur.execute("SELECT * FROM proxies WHERE id={}".format(proxy_id))
		return self.cur.fetchall()

	def get_recent_proxy(self):
		with self.con:
			self.cur.execute("SELECT * FROM proxies ORDER BY id DESC LIMIT 1")
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