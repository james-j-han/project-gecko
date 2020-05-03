

class Search:

	def __init__(self, search_type, search):
		self.search_type = search_type
		self.search = search
		self.keywords = {}

		if self.search_type == 'Keywords':
			self.set_keywords()
		elif self.search_type == 'Variant':
			self.keywords['variant'] = self.search
		elif self.search_type == 'Direct Link':
			self.keywords['direct_link'] = self.search
		else:
			print('No matching search type')

	def set_keywords(self):
		pos = []
		neg = []
		for kw in self.search.split(' '):
			if '+' in kw[0]:
				w = kw[1:]
				pos.append(w.lower())
			elif '-' in kw[0]:
				w = kw[1:]
				neg.append(w.lower())

		self.keywords['pos'] = pos
		self.keywords['neg'] = neg