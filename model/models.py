class Tournament:

  def __init__(self, name, venue, date, description,
               time_control, players, ended=False):
    self.name = name
    self.venue = venue
    self.date = date
    self.description = description
    self.time_control = time_control
    self.players = players
    self.rounds = []
    self.ended = ended

  def make_pairings(self):
    pairings = []
    if len(self.rounds) >= 1:
      players = [str(p) for p in sorted(self.players)]
      last_pairings = [(match[0][0], match[1][0]) for rd in self.rounds
                       for match in rd.matches]
      while players:
        player = players.pop()
        for other in players[-1::-1]:
          pair = (player, other)
          if pair not in last_pairings and pair[-1::-1] not in last_pairings:
            pairings.append((player, other))
            players.remove(other)
            break
    else:
      players = [str(p) for p in sorted(self.players, key=lambda x:x.rank)]
      lower, upper = players[:len(players) // 2], players[len(players) // 2:]
      for player, other in zip(upper, lower):
        pairings.append((player, other))
    if not pairings:
      self.ended = True
    return pairings

  def serialize(self):
    serialized = {
        'name': self.name,
        'venue': self.venue,
        'date': self.date,
        'description': self.description,
        'time_control': self.time_control,
        'ended': self.ended
    }
    serialized['players'] = []
    serialized['rounds'] = []
    for player in self.players:
      serialized['players'].append(player.__dict__)
    for rd in self.rounds:
      serialized['rounds'].append(rd.__dict__)
    return serialized


class Player:
  def __init__(self, first_name, last_name, birthdate, gender, rank, score=0):
    self.first_name = first_name
    self.last_name = last_name
    self.birthdate = birthdate
    self.gender = gender
    self.rank = rank
    self.score = score

  def update_score(self, score):
    self.score += score

  def __str__(self):
    return f'{self.first_name.title()} {self.last_name.title()}'

  def __gt__(self, other):
    if self.score == other.score:
      return self.rank > other.rank
    else:
      return self.score > other.score

  def __lt__(self, other):
    if self.score == other.score:
      return self.rank < other.rank
    else:
      return self.score < other.score


class Round:
  def __init__(self, name, start_timestamp, matches, end_timestamp=''):
    self.name = name
    self.start_timestamp = start_timestamp
    self.end_timestamp = end_timestamp
    self.matches = matches
