#!/usr/bin/env python3

class Game:
	def __init__(self):
		self.players = []
		self.places = [0] * 6
		self.purses = [0] * 6
		self.in_penalty_box = [0] * 6

		self.pop_questions = [f'Pop Question {i}' for i in range(50)]
		self.science_questions = [f'Science Question {i}' for i in range(50)]
		self.sports_questions = [f'Sports Question {i}' for i in range(50)]
		self.rock_questions = [f'Rock Question {i}' for i in range(50)]

		self.current_player = 0
		self.is_getting_out_of_penalty_box = False

	def is_playable(self):
		return self.how_many_players >= 2

	def add(self, player_name):
		self.players.append(player_name)
		self.in_penalty_box[self.how_many_players] = False
		print(player_name + " was added")
		print("They are player number %s" % len(self.players))

	@property
	def how_many_players(self):
		return len(self.players)

	def player_place(self,roll):
		self.places[self.current_player] = self.places[self.current_player] + roll
		if self.places[self.current_player] > 11:
			self.places[self.current_player] = self.places[self.current_player] - 12
		return self.places[self.current_player]

	def roll(self, roll):
		print(f'{self.players[self.current_player]} is the current player')
		print(f'They have rolled a {roll}')

		if self.in_penalty_box[self.current_player]:
			if roll % 2 == 0:
				print(f'{self.players[self.current_player]} is not getting out of the penalty box')
				self.is_getting_out_of_penalty_box = False
				return
			else:
				self.is_getting_out_of_penalty_box = True
				print(f'{self.players[self.current_player]} is getting out of the penalty box')

		self.places[self.current_player] = self.player_place(roll)
		print(self.players[self.current_player] + \
					'\'s new location is ' + \
					str(self.places[self.current_player]))
		print(f'The category is {self._current_category}')
		self._ask_question()

	def _ask_question(self):
		if self._current_category == 'Pop': print(self.pop_questions.pop(0))
		if self._current_category == 'Science': print(self.science_questions.pop(0))
		if self._current_category == 'Sports': print(self.sports_questions.pop(0))
		if self._current_category == 'Rock': print(self.rock_questions.pop(0))

	@property
	def _current_category(self):
		if self.places[self.current_player] % 4 == 0: return 'Pop'
		if self.places[self.current_player] % 4 == 1: return 'Science'
		if self.places[self.current_player] % 4 == 2: return 'Sports'
		if self.places[self.current_player] % 4 == 3: return 'Rock'

	def was_correctly_answered(self):
		if self.in_penalty_box[self.current_player] and not self.is_getting_out_of_penalty_box:
			winner = True
		else:
			print("Answer was correct!!!!")

			self.purses[self.current_player] += 1
			
			print(self.players[self.current_player] + \
				' now has ' + \
				str(self.purses[self.current_player]) + \
				' Gold Coins.')
			winner = self._did_player_win()
			
		self.current_player = self.next_player()
		return winner

	def wrong_answer(self):
		print('Question was incorrectly answered')
		print(self.players[self.current_player] + " was sent to the penalty box")
		self.in_penalty_box[self.current_player] = True
		self.current_player = self.next_player()

	def _did_player_win(self):
		return not (self.purses[self.current_player] == 6)

	def next_player(self):
		self.current_player += 1
		if self.current_player == len(self.players): 
			self.current_player = 0
		return self.current_player


from random import randrange, seed
import sys
seed(int(sys.argv[1]))

if __name__ == '__main__':
	not_a_winner = False

	game = Game()

	game.add('Chet')
	game.add('Pat')
	game.add('Sue')

	while True:
		game.roll(randrange(5) + 1)

		if randrange(9) == 7:
			game.wrong_answer()
			not_a_winner = True
		else:
			not_a_winner = game.was_correctly_answered()

		if not not_a_winner: break
