import numpy as np
from die import Die

class Perudo_player():
	#This will become an Agent type class
	def __init__(self, name, dice_number, game):
		self.name = name
		self.game = game
		self.palifico_round = -1
		self.dice = []
		self.dice_number = dice_number
		for i in range(0, dice_number):
			self.dice.append(Die())
		
	def roll_dice(self):
		for die in self.dice:
			die.roll()
		# Sort dice into value order e.g. 4 2 5 -> 2 4 5
		self.dice = sorted(self.dice, key=lambda die: die.value)

	def count_dice(self, value):
		number = 0
		for die in self.dice:
			if die.value == value or (not self.game.is_palifico_round() and die.value == 1):
				number += 1
		return number
	
	def Dice_numbers(self):
		dice_insert = np.zeros((self.dice_number))
		for i in range(0,len(self.dice)):
			dice_insert[i] = self.dice[i].value
		return dice_insert