from model.models import Tournament, Player, Round
from .mappers import DBGateway, Mapper

class Validator:
	def prompt(self, message):
		while True:
			print(message)
			a_number = input()
			try:
				a_number = int(a_number)
			except:
				print('Please enter numeric digits.')
				continue
			if a_number < 2 and 'players' in message:
				print('Enter at least 2 players.')
				continue
			break
		return a_number

class Controller(Validator, Mapper):
	def __init__(self):
		Mapper.__init__(self)

	def create_tournament(self):
		t = {}
		print('Enter tournament name')
		t['name'] = input()
		print('Enter the venue')
		t['venue'] = input()
		print('Enter the date')
		t['date'] = input('mm/dd/yyyy: ')
		print('Enter a time control')
		t['time_control'] = input('Bullet, Rapid, Blitz: ')
		print('Enter a description')
		t['description'] = input()
		print(' Add Players '.center(100, '-'))
		nbr_players = self.prompt('How many players?')
		players = []
		while len(players) < nbr_players:
			print(f' Player {len(players)+1} '.center(100, '-'))
			players.append(self.add_player())
		players = [Player(**p) for p in players]
		self.tournament = Tournament(**t, players=players)
		rd = self.start_round('Round 1', self.tournament.make_pairings())
		self.tournament.rounds.append(rd)

	def select_tournament(self):
		tournaments = self.load_tournaments()
		print('Select a Tournament')
		for t in tournaments:
			selected = input(f'Tournament: {t.name.title()} [Enter] continue, [Y] List: ')
			if selected.lower() == 'y':
				return t.name
		return ''

	def add_player(self):
		player = {}
		print('Enter first name')
		player['first_name'] = input()
		print('Enter last name')
		player['last_name'] = input()
		print('Enter date of birth')
		player['birthdate'] = input()
		print('Enter gender')
		player['gender'] = input('Female, Male: ')
		player['rank'] = self.prompt('Enter player rank')
		return player

	def start_round(self, name, pairings):
		print('Enter start date and time [Round 1]')
		start_datetime = input('mm/ddd/yyyy HH:MM: ')
		matches = []
		for player, other in pairings:
			matches.append(([player, None], [other, None]))
		return Round('Round 1', start_datetime, matches)

	def save_tournament(self):
		self.db_gateway.save(self.tournament.serialize())





