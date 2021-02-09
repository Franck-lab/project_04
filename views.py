from controllers import Controller
from utils import Formater

class UI:
	def __init__(self):
		self.ctrl = Controller()
		self.view = View()
		self.choice = 'M'

	def go_back(self):
		print('[M] Back to menu [Q] Quit')
		self.choice = input()

	def idle(self):
		if self.choice == '1':
			print(' New Tournament '.center(100, '='))
			self.ctrl.create_tournament()
			self.ctrl.save_tournament()
			print('Creation Complete!!!!')
			self.go_back()
		elif self.choice == '2':
			self.view.show_tournaments(self.ctrl.load_tournaments())
			self.go_back()
		elif self.choice == '3':
			self.view.show_players(self.ctrl.load_players())
			self.go_back()
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
					'[3] List All Players'
					'[Q] Quit', sep='\n'
		)

	def show_tournaments(self, tournaments):
		table = [
				['#', 'Name', 'Description', 'Venue', 'Date', 'Time Control'],
		]
		ID = (str(n + 1) for n in range(10000))
		for tournament in tournaments:
			table.append([next(ID), tournament.name, tournament.description, tournament.venue, tournament.date, tournament.time_control])
		self.print_table(table, self.parse_table(table))

	def show_players(self, players):
		table = [
				['#', 'Name', 'Date of Birth', 'Gender', 'Rating', 'Score'],
		]
		ID = (str(n + 1) for n in range(10000))
		for player in players:
			table.append([next(ID), str(player), player.birthdate, player.gender, str(player.rank), str(player.score)])
		self.print_table(table, self.parse_table(table))
