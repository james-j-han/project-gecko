from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEngineScript
from PyQt5.QtNetwork import QNetworkCookie

from poll_token import PollToken

import time

class Webview(QWebEngineView):

	send_token = pyqtSignal(str)
	captcha_loaded = pyqtSignal()
	load_waiting = pyqtSignal()
	update_task_status = pyqtSignal(str)
	request_abort = pyqtSignal()

	# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
	user_agent = 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'

	def __init__(self):
		super().__init__()
		# self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		self.incognito_profile = QWebEngineProfile()
		self.incognito_profile.setHttpUserAgent(self.user_agent)
		# print('[OFF-THE-RECORD]: {}'.format(self.incognito_profile.isOffTheRecord()))
		# self.settings = QWebEngineSettings()
		# self.settings.setAttribute(QWebEngineSettings.PictographFont)
		# self.cookie_store = self.profile.cookieStore()
		# self.cookie_store.cookieAdded.connect(self.on_cookie_added)
		self.new_page = QWebEnginePage(self.incognito_profile, self)
		# # self.page.settings().setAttribute(QWebEngineSettings.PictographFont)
		self.setPage(self.new_page)

		self.cookies = []
		# self.html = None
		# self.store = None
		# self.task_id = None
		self.t = PollToken()
		self.t.poll.connect(self.get_token)
		self.t.request_abort.connect(self.request_abort.emit)

	def load_url(self, url, captcha=False):
		self.new_page = QWebEnginePage(self.incognito_profile, self)
		self.setPage(self.new_page)
		print('[OFF-THE-RECORD]: {}'.format(self.page().profile().isOffTheRecord()))
		# self.store = url
		# if task_id:
		# 	self.task_id = task_id
		if captcha:
			self.page().loadFinished.connect(self.render_captcha)
		self.page().load(QUrl(url))

	def render_captcha(self):
		# script = '''
		# var loop = setInterval(function() {{
		# 	if (typeof grecaptcha === 'undefined' || typeof grecaptcha.render === 'undefined') {{
				
		# 	}} else {{
		# 		grecaptcha.render('test');
		# 		clearInterval(loop);
		# 	}}
		# }}, 100);
		# document.write("<head><div class='g-recaptcha' id='test' data-sitekey='{}'></div></head><body><script src='https://www.google.com/recaptcha/api.js?render=explicit' async defer></script></body>");
		# '''.format(sitekey)
		script = '''
		var loop = setInterval(function() {{
			if (document.getElementById('g-recaptcha') === null) {{
				
			}} else {{
				var d = document.getElementById('g-recaptcha');
				document.body.innerHTML = '';
				document.body.appendChild(d);
				clearInterval(loop);
			}}
		}}, 100);
		'''
		self.page().runJavaScript(script, self.div_call)

	def div_call(self, data):
		script = "document.getElementById('g-recaptcha');"
		self.page().runJavaScript(script, self.render_call)

	def render_call(self, data):
		if type(data) is dict:
			self.captcha_loaded.emit()
			self.t.start()

	# def render_page(self):
	# 	self.page.toHtml(self.html_call)

	# def html_call(self, data):
	# 	self.html = data
	# 	# print(self.html)

	def get_token(self):
		script = '''
		grecaptcha.getResponse();
		'''
		self.page().runJavaScript(script, self.token_call)

	def token_call(self, data):
		if data:
			print('[TOKEN]: {}'.format(data))
			token = data
			if len(token) > 0:
				self.send_token.emit(token)
				# self.load_waiting.emit()
				self.t.abort = True
				self.t.quit()

	def on_cookie_added(self, cookie):
		for c in self.cookies:
			if c.hasSameIdentifier(cookie):
				return
		self.cookies.append(QNetworkCookie(cookie))

	def set_cookies(self, cookies):
		for cookie in cookies:
			# print('name: {}'.format(cookie.name()))
			# print('value: {}'.format(cookie.value()))
			# print('domain: {}'.format(cookie.domain()))
			self.page.profile().cookieStore().setCookie(cookie)
			# self.cookie_store.setCookie(cookie)

	def get_cookies(self):
		pass
		# for cookie in self.cookies:
		# 	print('[DOMAIN] {}'.format(cookie.domain()))
		# 	print('[NAME] {}'.format(cookie.name()))
		# 	print('[VALUE] {}'.format(cookie.value()))
		# 	print()