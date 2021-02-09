from view.views import UI

class Application(UI):
	def __init__(self):
		UI.__init__(self)
		self.done = False

	def run(self):
		while not self.done:
			self.idle()


if __name__ == '__main__':
	app = Application()
	app.run()





