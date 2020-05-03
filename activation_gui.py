from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from licensing.models import *
from licensing.methods import Key, Helpers
from activation_ui import Ui_Form
from stylesheet import Stylesheet

import time

class ActivationGUI(QtWidgets.QDialog):

	RSAPubKey = '<RSAKeyValue><Modulus>p8JYim7liLizS/9s1Ew29iT9ZfAnAqX7nSryR7dTwGgL2pAD6rmIkmmYbFFLz0IGJ2S9+ZghaTOMTzgyAO/lK5KJs7+sQBMej7EW57r497kQbwtuSmnd+lF8dTgSmjEaQ6g/0wSZIPxr/THZ2nkaRGG5i12QGN31j84AihENm1YU2rV2rXlLttpdQ9VlRdKADZb1asWBei6He4CJiL4eqrjeh3SdRJ+fzirEoofNwi35zrGo6+AgH6svSvkTjlyZnwrv/DWSbXw3yKpKCEelRSEI90DSwwkKbenhAXiS5z+KPr8uRbmwX58kBPlmwHfzfpDk2j6mx/W6DrusZDMICw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>'
	auth = 'WyIxNTQzMyIsIm4vSjhMVWI4ZWxsZWZZRWRLc1hoN1p6cVYwbHlIWmh3Q2hHNk11VTQiXQ=='

	def __init__(self, db):
		super().__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)

		self.styles = Stylesheet()
		self.setStyleSheet(self.styles.dark_theme())

		logo = QtGui.QPixmap('src/logo.png')
		self.ui.label.setPixmap(QtGui.QPixmap(logo.scaled(1000, 1000, QtCore.Qt.KeepAspectRatio)))
		icon_key = QtGui.QIcon(QtGui.QPixmap('src/icon_key.png'))
		self.ui.push_button_activate.setIcon(icon_key)

		self.tgadb = db
		key_item = self.tgadb.get_key()
		print(key_item)
		self.key = None
		if key_item:
			for key_id, key_value in key_item:
				self.key = key_value
				self.ui.line_edit_key.setText(self.key)
		
		self.ui.push_button_activate.clicked.connect(self.verify)
		self.ui.line_edit_key.textChanged.connect(self.clear_focus)

	def clear_focus(self):
		if len(self.ui.line_edit_key.text()) == 0:
			self.ui.line_edit_key.clearFocus()

	def verify(self):
		# key = 'IQKLU-VIDOO-ULUHQ-ZOOYZ'
		key = self.ui.line_edit_key.text()
		result = Key.activate(token=self.auth, rsa_pub_key=self.RSAPubKey, product_id=5865, key=key, machine_code=Helpers.GetMachineCode())

		if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
			# print('The license does not work: {0}'.format(result[1]))
			ok = QtWidgets.QMessageBox.Ok
			title = 'Error'
			message = 'The license does not work: {0}'.format(result[1])
			d = QtWidgets.QMessageBox()
			d.setWindowTitle(title)
			d.setText(message)
			d.setStandardButtons(ok)
			d.exec_()
		else:
			print('The license is valid!')
			if key == self.key:
				print('Keys are the same')
			elif key != self.key:
				print('Keys are not the same, updating key...')
				self.tgadb.save_key(key, 1)
			else:
				self.tgadb.save_key(key)
			self.accept()