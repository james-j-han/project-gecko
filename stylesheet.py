


class Stylesheet:

	def __init__(self):
		pass
		# background_color = '#FBFAFA'
		# text_color = '#1E2019'
		# border_color = '#617778'
		# secondary_color = '#488255'
		# disabled_color = '#d6d3d3'
		# line_color = '#02C93B'
		# selection_color = '#90B8C7'

	def dark_theme(self):
		background_color = '#1E2019'
		text_color = '#DFE9E7'
		border_color = '#617778'
		secondary_color = '#488255'
		disabled_color = '#303328'
		line_color = '#02C93B'
		selection_color = '#97C777'
		stylesheet = f'''
		* {{
			font-size: 14px;
<<<<<<< HEAD
			font-family: 'Century Gothic', 'Helvetica';
=======
			font-family: 'Montserrat';
>>>>>>> f8132ff9766b1e191df0da219093b71429e939e0
		}}
		QMainWindow {{
			background-color: {background_color};
			border-radius: 10px;
		}}
		QSplitter:handle {{
			background: {secondary_color};
		}}
		QLine {{
			background-color: {secondary_color};
		}}
		QStatusBar {{
			color: {text_color};
		}}
		QScrollBar:vertical {{
			width: 20px;
			background-color: {background_color};
			border: solid {selection_color};
			margin: 20px 0px 20px 0px;
		}}
		QScrollBar:handle:vertial {{
			background-color: {background_color};
			border: 1px solid {selection_color};
			min-width: 20px;
		}}
		QScrollBar:up-arrow:vertical {{
			image: url(src/icon_down_arrow.png);
			background-color: {selection_color};
			border: none;
		}}
		QScrollBar:down-arrow:vertical {{
			image: url(src/icon_light_down_arrow.png);
			background-color: {background_color};
			border: none;
		}}
		QGroupBox {{
			color: {text_color};
			border: none;
		}}
		QGroupBox#group_box_options {{
			padding-top: 25px;
		}}
		QGroupBox#group_box_log {{
			margin-top: 10px;
			padding-top: 25px;
		}}
		QGroupBox#group_box_tasks {{
			margin-top: 10px;
		}}
		QGroupBox:indicator {{
			width: 14px;
			height: 14px;
			border-style: solid;
			border-width: 1px;
			border-color: {selection_color};
			background-color: {background_color};
		}}
		QGroupBox:indicator:checked {{
			width: 14px;
			height: 14px;
			image: url(src/icon_checked.png);
			background-color: {selection_color};
		}}
		QPushButton {{
			font-weight: normal;
			width: 40px;
			height: 30px;
			color: {text_color};
			background-color: {background_color};
			border-style: inset;
			border-width: 2px;
			border-radius: 15px;
			border-color: {secondary_color};
			padding: 2px;
		}}
		QPushButton:disabled {{
			background-color: {disabled_color};
			border-color: {disabled_color};
			border-style: solid;
		}}
		QPushButton:hover {{
			font-weight: bold;
			color: {background_color};
			background-color: {selection_color};
		}}
		QPushButton:pressed {{
			border-style: outset;
		}}
		QComboBox {{
			color: {text_color};
			border-style: solid;
			border-color: {selection_color};
			border-width: 1px;
			border-radius: 2px;
			background-color: {background_color};
		}}
		QComboBox:disabled {{
			color: {background_color};
			background-color: {disabled_color};
			border: none;
		}}
		QComboBox QAbstractItemView {{
			background-color: {background_color};
			color: {text_color};
			selection-background-color: {selection_color};
			selection-color: {background_color};
		}}
		QComboBox:drop-down {{
			border: 0px;
		}}
		QComboBox:down-arrow {{
			image: url(src/icon_light_down_arrow.png);
			width: 14px;
			height: 14px;
			margin-right: 2px;
		}}
		QComboBox:down-arrow:disabled {{
			image: url(src/icon_disabled_down_arrow.png);
		}}
		QLineEdit {{
			color: {text_color};
			border-style: solid;
			border-color: {selection_color};
			border-width: 1px;
			border-radius: 2px;
			background-color: {background_color};
			padding-left: 3px;
		}}
		QLineEdit:disabled {{
			background-color: {disabled_color};
			border: none;
		}}
		QLabel {{
			color: {text_color};
			padding-left: 3px;
		}}
		QLabel:disabled {{
			color: {disabled_color};
		}}
		#label_picture {{
			border: none;
		}}
		#label_image {{
			border: none;
		}}
		QCheckBox {{
			color: {text_color};
			padding-left: 6px;
		}}
		QCheckBox:indicator {{
			width: 14px;
			height: 14px;
			border-style: solid;
			border-width: 1px;
			border-color: {selection_color};
			background-color: {background_color};
		}}
		QCheckBox:indicator:checked {{
			width: 14px;
			height: 14px;
			image: url(src/icon_checked.png);
			background-color: {selection_color};
		}}
		QCheckBox:indicator:disabled {{
			border-color: {disabled_color};
		}}
		QCheckBox:disabled {{
			color: {disabled_color};
			border: none;
		}}
		QHeaderView {{
			color: {text_color};
			background-color: {background_color};
		}}
		QHeaderView:section:vertical {{
			border-top: 2px solid;
			border-left: 2px solid;
			border-bottom: 2px solid;
			border-color: {selection_color};
			margin-bottom: 10px;
			padding-left: 10px;
			border-top-left-radius: 25px;
			border-bottom-left-radius: 25px;
		}}
		QHeaderView:section {{
			font: bold;
			color: {text_color};
			background-color: {background_color};
			border-style: outset;
		}}
		QTableWidget {{
			outline: none;
			color: {text_color};
			background-color: {background_color};
			border: none;
		}}
		QTableWidget:item {{
			border-top: 2px solid;
			border-bottom: 2px solid;
			margin-bottom: 10px;
			border-color: {selection_color};
		}}
		QTableWidget:item:selected {{
			selection-color: {background_color};
			background-color: {selection_color};
		}}
		QTableCornerButton:section {{
			background-color: {background_color};
		}}
		QTabWidget {{
			border: none;
			background-color: {background_color};
		}}
		QTabWidget:pane {{
			border: none;
		}}
		#tab_widget_tasks:tab {{
			width: 40px;
			height: 40px;
			color: {text_color};
			background-color: {background_color};
			border-style: solid;
			border-width: 3px;
			border-top: none;
			border-bottom: none;
			border-color: {selection_color};
			padding-bottom: 8px;
			padding-left: 3px;
		}}
		#tab_widget_tasks:tab:first {{
			margin-top: 10px;
		}}
		#tab_widget_tasks:tab:hover {{
			color: {background_color};
			background-color: {selection_color};
		}}
		#tab_widget_tasks:tab:selected {{
			color: {background_color};
			background-color: {selection_color};
		}}
		QListWidget {{
			border-style: solid;
			border-width: 1px;
			border-color: {selection_color};
			border-radius: 2px;
			background-color: {background_color};
			color: {text_color};
		}}
		QListWidget:item:selected, QListWidget:item:hover {{
			background-color: {selection_color};
			color: {background_color};
		}}
		QPlainTextEdit {{
			border-style: solid;
			border-width: 1px;
			border-color: {selection_color};
			border-radius: 2px;
			background-color: {background_color};
			color: {text_color};
		}}
		QDialog {{
			background-color: {background_color};
			color: {text_color};
		}}
		QDialog QLabel {{
			border: none;
		}}
		#recaptcha_ui {{
			background-color: {background_color};
		}}
		#tab_widget_captcha:tab {{
			height: 30px;
			color: {text_color};
			background-color: {background_color};
			border-style: solid;
			border-width: 3px;
			border-left: none;
			border-right: none;
			border-color: {selection_color};
			padding-left: 5px;
			padding-right: 5px;
		}}
		#tab_widget_captcha:tab:hover {{
			font: bold;
			color: {background_color};
			background-color: {selection_color};
		}}
		#tab_widget_captcha:tab:selected {{
			font: bold;
			color: {background_color};
			background-color: {selection_color};
		}}
		#label_gif:hover {{
			border: none;
		}}
		#push_button_new_tab {{
			image: url(src/icon_light_new_tab.png);
		}}
		#push_button_new_tab:hover {{
			image: url(src/icon_new_tab.png);
		}}
		#button_delete {{
			image: url(src/icon_light_x.png);
		}}
		#button_delete:hover {{
			image: url(src/icon_x.png);
		}}
		#button_delete:disabled {{
			image: url(src/icon_disabled_x.png);
		}}
		#button_play {{
			image: url(src/icon_light_play.png);
		}}
		#button_play:hover {{
			image: url(src/icon_play.png);
		}}
		#button_play:disabled {{
			image: url(src/icon_disabled_play.png);
		}}
		#button_stop {{
			image: url(src/icon_light_stop.png);
		}}
		#button_stop:hover {{
			image: url(src/icon_stop.png);
		}}
		#button_stop:disabled {{
			image: url(src/icon_disabled_stop.png);
		}}
		#push_button_captcha {{
			image: url(src/icon_light_captcha.png);
		}}
		#push_button_captcha:hover {{
			image: url(src/icon_captcha.png);
		}}
		#push_button_delete_all_profiles, #push_button_delete_all_billing, #push_button_delete_all_proxies, #pb_delete_all_accounts {{
			image: url(src/icon_light_delete_all_2.png);
		}}
		#push_button_delete_all_profiles:hover, #push_button_delete_all_billing:hover, #push_button_delete_all_proxies:hover, #pb_delete_all_accounts:hover {{
			image: url(src/icon_delete_all_2.png);
		}}
		#push_button_save_task, #push_button_save_profile, #push_button_save_billing, #push_button_save_proxies, #pb_save_account, #pb_save_settings {{
			image: url(src/icon_light_save.png);
		}}
		#push_button_save_task:hover, #push_button_save_profile:hover, #push_button_save_billing:hover, #push_button_save_proxies:hover, #pb_save_account:hover, #pb_save_settings:hover {{
			image: url(src/icon_save.png);
		}}
		#push_button_new_task, #push_button_new_profile, #push_button_new_billing, #push_button_new_proxies, #pb_new_account {{
			image: url(src/icon_light_new.png);
		}}
		#push_button_new_task:hover, #push_button_new_profile:hover, #push_button_new_billing:hover, #push_button_new_proxies:hover, #pb_new_account:hover {{
			image: url(src/icon_new.png);
		}}
		#push_button_import_proxies {{
			image: url(src/icon_light_import.png);
		}}
		#push_button_import_proxies:hover {{
			image: url(src/icon_import.png);
		}}
		#push_button_delete_task, #push_button_delete_profile, #push_button_delete_billing, #push_button_delete_proxies, #pb_delete_account {{
			image: url(src/icon_light_delete.png);
		}}
		#push_button_delete_task:hover, #push_button_delete_profile:hover, #push_button_delete_billing:hover, #push_button_delete_proxies:hover, #pb_delete_account:hover {{
			image: url(src/icon_delete.png);
		}}
		#push_button_test_all_proxies, #push_button_test_custom_shopify {{
			image: url(src/icon_light_test.png);
		}}
		#push_button_test_all_proxies:hover, #push_button_test_custom_shopify:hover {{
			image: url(src/icon_test.png);
		}}
		#pb_open_login {{
			image: url(src/icon_light_login.png);
		}}
		#pb_open_login:hover {{
			image: url(src/icon_login.png);
		}}
		#push_button_gmail {{
			image: url(src/icon_light_gmail.png);
		}}
		#push_button_gmail:hover {{
			image: url(src/icon_gmail.png);
		}}
		#check_box_mask_proxies {{
			image: url(src/icon_light_mask.png);
		}}
		#check_box_mask_proxies:indicator:indeterminate {{
			image: url(src/icon_partially_checked.png);
			background-color: {selection_color};
		}}
		#label_tested {{
			color: {text_color};
			background-color: {disabled_color};
			border-style: solid;
			border-color: {disabled_color};
			border-width: 1px;
			border-radius: 2px;
			padding-left: 3px;
		}}
		#tw_accounts {{
			alternate-background-color: {disabled_color};
		}}
		#tw_accounts:item {{
			border: none;
			margin-bottom: 0px;
		}}
		#tw_accounts:item:selected {{
			selection-color: {background_color};
			background-color: {selection_color};
		}}
		#tw_accounts QHeaderView:section:vertical {{
			border: none;
			margin-bottom: 0px;
		}}
		#pb_account_play {{
			border: 2px inset;
			border-color: {secondary_color};
			border-radius: 10px;
			image: url(src/icon_light_play.png);
		}}
		#pb_account_play:hover {{
			image: url(src/icon_play.png);
		}}
		#pb_account_play:pressed {{
			border-style: outset;
		}}
		#pb_account_refresh {{
			border: 2px inset;
			border-color: {secondary_color};
			border-radius: 10px;
			image: url(src/icon_light_refresh.png);
		}}
		#pb_account_refresh:hover {{
			border-style: outset;
			image: url(src/icon_refresh.png);
		}}
		#pb_account_refresh:pressed {{
			border-style: outset;
		}}
		#pb_account_delete {{
			border: 2px inset;
			border-color: {secondary_color};
			border-radius: 10px;
			image: url(src/icon_light_x.png);
		}}
		#pb_account_delete:hover {{
			border-style: outset;
			image: url(src/icon_x.png);
		}}
		#pb_account_delete:pressed {{
			border-style: outset;
		}}
		#button_gif {{
			background-color: {background_color};
			border-style: solid;
			border-width: 0px;
			border-radius: 15px;
			border-color: {secondary_color};
		}}
		'''
		return stylesheet