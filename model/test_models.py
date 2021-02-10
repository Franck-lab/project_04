from .models import Tournament, Player, Round


players = [Player('bob', 'smith', 'x', 'x', rank=45),
           Player('alice', 'queen', 'x', 'x', rank=50),
           Player('paul', 'jones', 'x', 'x', rank=25),
           Player('patt', 'sanders', 'x', 'x', rank=3)]


def test_tournament_model():
  t = Tournament('name', 'venue', 'date', 'description', 'time_control',
                 ['player_1', 'player_2', 'player_3', '...'])
  assert t.name
  assert t.venue
  assert t.date
  assert t.description
  assert t.time_control
  assert type(t.players) == list
  assert t.rounds == []
  assert not t.ended


def test_player_model():
  player = Player('first_name', 'last_name', 'birthdate', 'gender', rank=20)
  assert player.first_name
  assert player.last_name
  assert player.birthdate
  assert player.gender
  assert player.rank
  assert player.score == 0
  assert str(player) == 'First_Name Last_Name'


def test_compare_two_players():
  player = Player('bob', 'smith', 'x', 'x', rank=45)
  other = Player('alice', 'queen', 'x', 'x', rank=50)

  assert player < other
  assert other > player
  player.update_score(1)
  assert player.score == 1
  assert player > other
  assert other < player


def test_make_pairings_for_first_round():
  t = Tournament('name', 'venue', 'date',
                 'description', 'time_control', players)
  pairings = t.make_pairings()
  expected = [('Alice Queen', 'Patt Sanders'),
              ('Bob Smith', 'Paul Jones')]
  for pair in pairings:
    assert pair in expected or pair[-1::-1] in expected


def test_make_pairings_for_subsequence_rounds():
  t = Tournament('name', 'venue', 'date',
                 'description', 'time_control', players)
  rd = Round('name', 'mm/dd/yyyy HH:MM', [(['Alice Queen', 1],
             ['Patt Sanders', 0]), (['Bob Smith', 0.5], ['Paul Jones', 0.5])])
  t.rounds.append(rd)
  pairings = t.make_pairings()
  expected = [('Alice Queen', 'Bob Smith'),
              ('Paul Jones', 'Patt Sanders')]
  for pair in pairings:
    assert pair in expected or pair[-1::-1] in expected
  rd = Round('name', 'mm/dd/yyyy HH:MM',
             [(['Alice Queen', 1], ['Bob Smith', 0]),
              (['Patt Sanders', 0.5], ['Paul Jones', 0.5])])
  t.rounds.append(rd)
  pairings = t.make_pairings()
  expected = [('Alice Queen', 'Paul Jones'),
              ('Bob Smith', 'Patt Sanders')]
  for pair in pairings:
    assert pair in expected or pair[-1::-1] in expected
  rd = Round('name', 'mm/dd/yyyy HH:MM', [(['Alice Queen', 1],
             ['Paul Jones', 0]), (['Patt Sanders', 1], ['Bob Smith', 0])])
  t.rounds.append(rd)
  assert t.make_pairings() == []
  assert t.ended


def test_serialize_tournament_models():
  t = Tournament('name', 'venue', 'date',
                 'description', 'time control',
                 [Player('x', 'x', 'x', 'x', 6),
                  Player('xx', 'xx', 'xx', 'xx', 9)])

  serialized = t.serialize()
  expected = {'name': 'name',
              'venue': 'venue',
              'date': 'date',
              'description': 'description',
              'time_control': 'time control',
              'ended': False,
              'players': [{'first_name': 'x',
                           'last_name': 'x',
                           'birthdate': 'x',
                           'gender': 'x',
                           'rank': 6,
                           'score': 0},
                          {'first_name': 'xx',
                           'last_name': 'xx',
                           'birthdate': 'xx',
                           'gender': 'xx',
                           'rank': 9,
                           'score': 0}],
              'rounds': []}
  assert serialized == expected
  rd = Round('name', 'mm/dd/yyyy HH:MM',
             [(['player_1', 1], ['other', 0]),
              (['player_2', 0.5], ['another', 0.5])])
  t.rounds.append(rd)
  expected['rounds'] = [{'name': 'name',
                         'start_timestamp': 'mm/dd/yyyy HH:MM',
                         'end_timestamp': '',
                         'matches': [(['player_1', 1], ['other', 0]),
                                     (['player_2', 0.5], ['another', 0.5])]}]
  assert expected == t.serialize()


def test_round_model():
  rd = Round('name', 'start_timestamp', ['match_1', 'match_2', 'match_3'], '')
  assert rd.name
  assert rd.start_timestamp
  assert rd.end_timestamp == ''
  assert type(rd.matches) == list
