from controller.controllers import Controller
from .utils import Formater

class UI:
	def __init__(self):
		self.ctrl = Controller()
		self.view = View()
		self.choice = 'M'

	def idle(self):
		if self.choice == '1':
			print(' New Tournament '.center(100, '='))
			self.ctrl.create_tournament()
			print('Creation Complete!!!!')
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '2':
			self.view.show_tournaments(self.ctrl.tournaments)
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '3':
			print('Sorted: [1] Alphabetically, [2] By rank')
			key = input()
			players = [p for t in self.ctrl.tournaments for p in t.players]
			self.view.show_players(players, key=key)
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '4':
			print('Sorted: [1] Alphabetically, [2] By rank')
			key = input()
			self.ctrl.select_tournament()
			if self.ctrl.selected:
				self.view.show_players(self.ctrl.selected.players, key=key)
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '5':
			self.ctrl.select_tournament()
			if self.ctrl.selected:
				self.view.show_rounds(self.ctrl.selected.rounds)
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '6':
			self.ctrl.select_tournament()
			if self.ctrl.selected:
				self.view.show_matches(self.ctrl.selected.rounds)
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '7':
			self.ctrl.select_tournament()
			if self.ctrl.selected:
				self.ctrl.upload_results()
				print('Updates Complete!!!!')
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice == '8':
			self.ctrl.select_tournament()
			if self.ctrl.selected:
				self.ctrl.update_ratings()
				print('Updates Complete!!!!')
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice.lower() == 'q':
			self.done = True
		else:
			self.view.display_menu()
			self.choice = input('Enter your choice: ')

class View(Formater):
	def display_menu(self):
		print(' Tournament Manager - Menu '.center(100, '='))
		print('[1] Create New Tournament',
					'[2] List Tournament',
					'[3] List All Players',
					'[4] List Players in a Tournament',
					'[5] List Rounds in a Tournament',
					'[6] List Matches in a Tournament',
					'[7] Upload Results',
					'[8] Update Player Rating',
					'[Q] Quit', sep='\n'
		)

	def show_tournaments(self, tournaments):
		table = [
				['#', 'Name', 'Description', 'Venue', 'Date', 'Time Control'],
		]
		ID = (str(n + 1) for n in range(10000))
		for t in tournaments:
			table.append([next(ID), t.name, t.description, t.venue, t.date, t.time_control])
		self.print_table(table, self.parse_table(table))

	def show_players(self, players, key):
		if key == '1': # by name
			players.sort(key=str)
		else:
			players.sort(key=lambda x:x.rank)
		table = [
				['#', 'Name', 'Date of Birth', 'Gender', 'Rating', 'Score'],
		]
		ID = (str(n + 1) for n in range(10000))
		for player in players:
			table.append([next(ID), str(player), player.birthdate, player.gender, str(player.rank), str(player.score)])
		self.print_table(table, self.parse_table(table))

	def show_rounds(self, rounds):
		table = [
				['#', 'Name', 'Start Datetime', 'End Datetime'],
		]
		ID = (str(n + 1) for n in range(10000))
		for rd in rounds:
			table.append([next(ID), rd.name, rd.start_timestamp, rd.end_timestamp])
		self.print_table(table, self.parse_table(table))

	def show_matches(self, rounds):
		table = [
				['#', 'Round', 'Matches'],
		]
		ID = (str(n + 1) for n in range(10000))
		for rd in rounds:
			for match in rd.matches:
				opponent_1 = f'{match[0][0]} [{match[0][1]}]'.rjust(25)
				opponent_2 = f'[{match[1][1]}] {match[1][0]}'.ljust(25)
				table.append([next(ID), rd.name, opponent_1 + ' - ' + opponent_2])
		self.print_table(table, self.parse_table(table))




