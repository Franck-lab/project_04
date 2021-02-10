from model.models import *
from tinydb import TinyDB

class DBGateway:
	def __init__(self, filename):
		self.db = TinyDB(filename)

	def save(self, serialized):
		t_table = self.db.table('tournaments')
		t_table.insert(serialized)

	def load(self):
		t_table = self.db.table('tournaments')
		return t_table.all()

class Mapper:
	def __init__(self):
		self.db_gateway = DBGateway('db.json')

	def load_tournaments(self):
		serialized = self.db_gateway.load()
		tournaments = []
		for t in serialized:
			serialized_players = t.pop('players')
			players = [Player(**p) for p in serialized_players]
			serialized_rounds = t.pop('rounds')
			rounds = [Round(**rd) for rd in serialized_rounds]
			t = Tournament(**t, players=players)
			t.rounds = rounds
			tournaments.append(t)
		return tournaments

	def load_players(self, tournament_name=None):
		serialized = self.db_gateway.load()
		if tournament_name:
			for t in serialized:
				if t['name'] == tournament_name:
					players = [Player(**p) for p in t['players']]
					break
		elif tournament_name == '':
			return []
		else:
			players = []
			for t in serialized:
				players.extend([Player(**p) for p in t['players']])
		return players
