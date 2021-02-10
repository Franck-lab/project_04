from model.models import Tournament, Player, Round
from .mappers import Mapper


class Validator:

  def prompt(self, message):
    while True:
      print(message)
      a_number = input()
      try:
        a_number = int(a_number)
      except ValueError:
        print('Please enter numeric digits.')
        continue
      if a_number < 2 and 'players' in message:
        print('Enter at least 2 players.')
        continue
      if 'result' in message and a_number not in (1, 2, 3):
        print('Enter a valid score. [1-3]')
        continue
      if 'rank' in message and a_number < 0:
        print('Please a positive number.')
        continue
      break
    return a_number


class Controller(Validator, Mapper):

  def __init__(self):
    Mapper.__init__(self)
    self.tournaments = []
    self.tournaments.extend(self.load_tournaments())
    self.selected = None

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
    tournament = Tournament(**t, players=players)
    rd = self.start_round('Round 1', tournament.make_pairings())
    tournament.rounds.append(rd)
    self.tournaments.append(tournament)
    self.save_tournaments()

  def select_tournament(self):
    print(' Select a Tournament '.center(100, '-'))
    for t in self.tournaments:
      selected = f'Tournament: {t.name.title()} [Enter] continue, [Y] List: '
      selected = input(selected)
      if selected.lower() == 'y':
        self.selected = t
        break
    else:
      self.selected = None

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
    if pairings:
      print(f'Enter start date and time {name}')
      start_datetime = input('mm/dd/yyyy HH:MM: ')
      matches = []
      for player, other in pairings:
        matches.append(([player, None], [other, None]))
      return Round(name, start_datetime, matches)
    else:
      return None

  def upload_results(self):
    if not self.selected.ended:
      players = [str(p) for p in self.selected.players]
      rd = self.selected.rounds[-1]
      print('Enter end date and time for this round')
      rd.end_timestamp = input('mm/dd/yyyy HH:MM: ')
      for i, match in enumerate(rd.matches):
        print(f'Match {i+1}: {match[0][0]} [X] - {match[1][0]}')
        score = self.prompt('Enter result X, (win [1], lose [2], tie [3]: ')
        if score == 1:
          match[0][1] = 1
          self.selected.players[players.index(match[0][0])].update_score(1)
          match[1][1] = 0
        elif score == 2:
          match[0][1] = 0
          match[1][1] = 1
          self.selected.players[players.index(match[1][0])].update_score(1)
        else:
          match[0][1] = .5
          self.selected.players[players.index(match[0][0])].update_score(.5)
          match[1][1] = .5
          self.selected.players[players.index(match[1][0])].update_score(.5)
      rd = self.start_round(f'Round {len(self.selected.rounds)+1}',
                            self.selected.make_pairings())
      if rd:
        self.selected.rounds.append(rd)
      self.save_tournaments()

  def update_ratings(self):
    for player in self.selected.players:
      entry = f'Player: {str(player)} [ENTER] Continue or [Y] Edit rank: '
      entry = input(entry)
      if entry.lower() == 'y':
        rank = self.prompt('Enter rank')
        player.rank = rank
        break
    self.save_tournaments()

  def save_tournaments(self):
    serialized = [t.serialize() for t in self.tournaments]
    self.gateway.save(serialized)
