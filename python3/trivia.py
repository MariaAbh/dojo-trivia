#!/usr/bin/env python3
categories = ["Pop","Science","Sports","Rock"]
class Player:
	def __init__(self, name):
		self.name = name
		self.place = 0
	def __str__(self):
		return self.name

class Game:
	def __init__(self):
		self.players = []
		self.purses = [0] * 6
		self.in_penalty_box = [0] * 6

		self.current_player = 0
		self.is_getting_out_of_penalty_box = False
		
		self.category_questions = {k:[f'{k} Question {i}' for i in range(50)] for k in categories}

	def is_playable(self):
		return self.how_many_players >= 2

	def add(self, player_name):

		self.players.append(Player(player_name))

		self.in_penalty_box[self.how_many_players] = False
		print(f"{player_name} was added")
		print(f"They are player number {len(self.players)}")

	@property
	def how_many_players(self):
		return len(self.players)

	def player_place(self,roll):
		self.players[self.current_player].place += roll
		if self.players[self.current_player].place > 11:
			self.players[self.current_player].place -= 12
		return self.players[self.current_player].place

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

		self.player_place(roll)
		print(f"{self.players[self.current_player]}'s new location is {self.players[self.current_player].place}")
		print(f'The category is {self._current_category}')
		self._ask_question()

	def _ask_question(self):
		print(self.category_questions[self._current_category].pop(0))

	@property
	def _current_category(self):
		return categories[self.players[self.current_player].place%len(categories)]

	def was_correctly_answered(self):
		if self.in_penalty_box[self.current_player] and not self.is_getting_out_of_penalty_box:
			winner = True
		else:
			print("Answer was correct!!!!")

			self.purses[self.current_player] += 1
			
			print(f"{self.players[self.current_player]} now has {self.purses[self.current_player]} Gold Coins.")
			winner = self._did_player_win()
			
		self.current_player = self.next_player()
		return winner

	def wrong_answer(self):
		print('Question was incorrectly answered')
		print(f"{self.players[self.current_player]} was sent to the penalty box")
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
