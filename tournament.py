from models import Tournament, Player, Round
from tinydb import TinyDB

def create_tournament():
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
	nbr_players = prompt('How many players?')
	players = []
	while len(players) < nbr_players:
		print(f' Player {len(players)} '.center(100, '-'))
		players.append(add_player())
	players = [Player(**p) for p in players]
	tournament = Tournament(**t, players=players)
	rd = start_round('Round 1', tournament.make_pairings())
	tournament.rounds.append(rd)
	return tournament

def start_round(name, pairings):
	print('Enter start date and time [Round 1]')
	start_datetime = input('mm/ddd/yyyy HH:MM: ')
	matches = []
	for player, other in pairings:
		matches.append(([player, None], [other, None]))
	return Round('Round 1', start_datetime, matches)

def add_player():
	player = {}
	print('Enter first name')
	player['first_name'] = input()
	print('Enter last name')
	player['last_name'] = input()
	print('Enter date of birth')
	player['birthdate'] = input()
	print('Enter gender')
	player['gender'] = input('Female, Male: ')
	player['rank'] = prompt('Enter player rank')
	return player

def save(serialized):
	db = TinyDB('db.json')
	t_table = db.table('tournaments')
	t_table.insert(serialized)

def prompt(message):
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

def display_menu():
	print(' Tournament Manager - Menu '.center(100, '='))
	print('[1] Create New Tournament',
				'[Q] Quit', sep='\n'
	)

if __name__ == '__main__':
	choice = 'M'
	while True:
		if choice == '1':
			print(' New Tournament '.center(100, '='))
			tournament = create_tournament()
			save(tournament.serialize())
			print('Creation Complete!!!!')
			print('[M] Back to menu [Q] Quit')
			choice = input()
		elif choice.lower() == 'q':
			break
		else:
			display_menu()
			choice = input('Enter your choice: ')




