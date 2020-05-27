from bs4 import BeautifulSoup

import requests
import json
import time
import os

# folder = os.path.dirname(os.path.abspath(__file__))
# # file = os.path.join(folder, 'disney_waiting_room.html')
# file = os.path.join(folder, 'disney_product_page.html')
# with open(file, 'r') as f:
# 	data = f.read()

# soup = BeautifulSoup(data, 'lxml')
# # title = soup.find('h1', {'id': 'heading'})
# title = soup.find('title')

# print(title)

# if title:
# 	if 'waiting' in title.text.lower():
# 		print('Waiting room!')
# else:
# 	print('Product page!')

url = 'https://www.shopdisney.com/minnie-mouse-the-main-attraction-ear-headband-for-adults-enchanted-tiki-room-limited-release-428405618185.html'

pid = url.split('-')[-1].split('.')[0]
print(pid)
