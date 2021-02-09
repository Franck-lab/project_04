from controllers import Controller

class UI:
	def __init__(self):
		self.ctrl = Controller()
		self.tournament = None
		self.choice = 'M'

	def idle(self):
		if self.choice == '1':
			print(' New Tournament '.center(100, '='))
			self.tournament = self.ctrl.create_tournament()
			self.ctrl.save_tournament(self.tournament)
			print('Creation Complete!!!!')
			print('[M] Back to menu [Q] Quit')
			self.choice = input()
		elif self.choice.lower() == 'q':
			self.done = True
		else:
			self.display_menu()
			self.choice = input('Enter your choice: ')

	def display_menu(self):
		print(' Tournament Manager - Menu '.center(100, '='))
		print('[1] Create New Tournament',
					'[Q] Quit', sep='\n'
		)