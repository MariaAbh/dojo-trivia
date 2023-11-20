#!/usr/bin/env python3
categories = ["Pop","Science","Sports","Rock"]
class Player:
	def __init__(self, name):
		self.name = name
		self.place = 0
		self.purse = 0
		self.in_penalty_box = False
		self.category = None
	def __str__(self):
		return self.name
	def roll(self,roll):
		self.place += roll
		self.place %= 12
		self.category = categories[self.place % len(categories)]
		return self.place

class Game:
	def __init__(self):
		self.players = []
		self.player = None
		self.current_player = -1
		self.is_getting_out_of_penalty_box = False
		
		self.category_questions = {k:[f'{k} Question {i}' for i in range(50)] for k in categories}

	def add(self, player_name):
		self.players.append(Player(player_name))
		print(f"{player_name} was added")
		print(f"They are player number {len(self.players)}")

	def roll(self, roll):
		self.next_player()
		print(f'{self.player} is the current player')
		print(f'They have rolled a {roll}')

		if self.player.in_penalty_box:
			if roll % 2 == 0:
				print(f'{self.player} is not getting out of the penalty box')
				self.is_getting_out_of_penalty_box = False
				return
			else:
				self.is_getting_out_of_penalty_box = True
				print(f'{self.player} is getting out of the penalty box')

		self.player.roll(roll)
		print(f"{self.player}'s new location is {self.player.place}")
		print(f'The category is {self.player.category}')
		print(self.category_questions[self.player.category].pop(0))

	def was_correctly_answered(self):
		if not self.player.in_penalty_box or self.is_getting_out_of_penalty_box:
			print("Answer was correct!!!!")
			self.player.purse += 1
			print(f"{self.player} now has {self.player.purse} Gold Coins.")
			
		return self.player.purse == 6

	def wrong_answer(self):
		print('Question was incorrectly answered')
		print(f"{self.player} was sent to the penalty box")
		self.player.in_penalty_box = True

	def next_player(self):
		self.current_player += 1
		if self.current_player == len(self.players):
			self.current_player = 0
		self.player = self.players[self.current_player]
		return self.current_player

from random import randrange, seed
import sys
seed(int(sys.argv[1]))

if __name__ == '__main__':
	# not_a_winner = False
	is_a_winner = False
	game = Game()
	game.add('Chet')
	game.add('Pat')
	game.add('Sue')

	while True:
		game.roll(randrange(5) + 1)
		if randrange(9) == 7:
			game.wrong_answer()
			# not_a_winner = True
			is_a_winner = False
		else:
			# not_a_winner = game.was_correctly_answered()
			is_a_winner = game.was_correctly_answered()
		if is_a_winner: break
