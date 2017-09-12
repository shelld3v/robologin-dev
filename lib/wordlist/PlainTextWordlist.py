class PlainTextWordlistParser:
	def __init__(self, fields=["username", "password"], separator=":"):
		self.fields = fields
		self.separator = separator

	def parse_content(self, path, default_values=None):
		pass

class 