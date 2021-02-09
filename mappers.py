from tinydb import TinyDB

class DBGateway:
	def __init__(self, filename):
		self.db = TinyDB(filename)

	def save(self, serialized):
		t_table = self.db.table('tournaments')
		t_table.insert(serialized)