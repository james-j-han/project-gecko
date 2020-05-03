

class Billing:

	def __init__(self, billing_id, billing_name, name_on_card, card_type, card_number, exp_month, exp_year, cvv):
		self.billing_id = billing_id
		self.billing_name = billing_name
		self.name_on_card = name_on_card
		self.card_type = card_type
		self.card_number = card_number
		self.exp_month = exp_month
		self.exp_year = exp_year
		self.cvv = cvv