import config
import random
import sys
import time
import numpy as np
from die import Die
from bet import Bet
from bet import DUDO
from strings import correct_dudo
from strings import incorrect_dudo
from strings import INSUFFICIENT_BOTS
from strings import INSUFFICIENT_DICE
from strings import round_title
from strings import welcome_message
from strings import winner
from bet import create_bet
import tensorflow as tf
from Perudo_player import Perudo_player

def flatten(l):
			return [item for sublist in l for item in sublist]

class Perudo_environment():
	def __init__(self,players,dice):
		self.starting_players = players
		self.starting_dice = dice
		self.players = []
		self.round = 0
		self.total_dice = players*dice
		self.bet_history = []
		self.Perudo_init()
		
	def reset(self):
		self.players = []
		self.round = 0
		self.total_dice = self.starting_players*self.starting_dice
		self.Perudo_init()


	def Perudo_init(self):
		#create the space for self.players with dice
		for i in range(0, self.starting_players):
			self.players.append(
				Perudo_player(
					name=i, 
					dice_number=self.starting_dice, 
					game=self
				)
			)
		self.Run_Perudo()

	def Round_begin(self):
		self.round += 1
		for player in self.players:
			player.roll_dice()
		self.round_over = False
		self.current_bet = None		
		random.shuffle(self.players)
		self.current_player = random.choice(self.players)
		self.bet_history = [self.state_format(0,True)]

	def state_format(self,bet,initial):
		if initial == False:
			one_hot = [int(i==self.current_player.name) for i in range(self.starting_players)]
			bet_quantity = bet.quantity
			bet_value = bet.value
		else:
			one_hot = np.zeros((self.starting_players))
			bet_quantity = 0
			bet_value = 0

		number_of_dice = len(self.current_player.dice)
		#original
		#concatenated = flatten([one_hot,[bet_quantity],[bet_value],[number_of_dice],[self.total_dice],[int(self.is_palifico_round())]])
		#normalised 
		concatenated = flatten([one_hot,[bet_quantity],[bet_value],[number_of_dice/6],[self.total_dice/(self.starting_dice*self.starting_players)],[int(self.is_palifico_round())]])
		return concatenated

	def step(self,raw_action):
		#choose next player and bid
		#next_bet = self.current_player.make_bet(action)
		try:
			action = self.action_translate(raw_action)
			next_bet = action
			print('next bet', next_bet)
			done = False
			failed = False
			if next_bet == DUDO:
				bet_string = 'Dudo!'
			else:
				bet_string = next_bet
			print('{0}: {1}'.format(self.current_player.name, bet_string))
			if next_bet == DUDO:
				self.pause(0.5)
				reward = self.run_dudo(self.current_player, self.current_bet)
				self.round_over = True
				while len(self.players) > 1:
					self.Round_begin()
			else:
				self.current_bet = next_bet
				self.bet_history = np.append(self.bet_history,[self.state_format(next_bet,False)],axis=0)
				self.current_player = self.get_next_player(self.current_player)
				#Made a legal bid
				reward = 2
		except Exception as e:
			print(f"Exception: {e}")
			quantity = raw_action%36 +1
			value = raw_action%6 + 1
			print("The game ends due to an illegal bid.")
			print(f'The bet was: {quantity}x{value}')
			#end the game
			done = True
			reward = -10
			failed = True 
			#self.round_over = True
		return reward, done, failed
	
	def action_translate(self,raw_action):
		#the input is 6*players + 1 long, the last is dudo
		if raw_action == (6*self.starting_players):
			#this is dudo
			return DUDO
		else:
			#1x1 2x1 3x1 ... 36x1 1x2 ...
			#this is bidding
			quantity = raw_action%36 + 1
			value = raw_action%6 + 1
			bet = create_bet(quantity, value, self.current_bet, self, self.current_player.game)
			return bet

	def Run_Perudo(self):
		if len(self.players) > 1:
			self.Round_begin()

	def run_dudo(self, player, bet):
		dice_count = self.count_dice(bet.value)
		if dice_count >= bet.quantity:
			print(incorrect_dudo(dice_count, bet.value))
			self.first_player = player
			self.remove_die(player)
			#incorrect dudo
			#could add more code to reduce the penalty for a plausable dudo
			reward = -1
		else:
			print(correct_dudo(dice_count, bet.value))
			previous_player = self.get_previous_player(player)
			self.first_player = previous_player
			self.remove_die(previous_player)
			#correct dudo
			reward = 4
		return reward

	def count_dice(self, value):
		number = 0
		for player in self.players:
			number += player.count_dice(value)
		return number

	def remove_die(self, player):
		player.dice.pop()
		msg = '{0} loses a die.'.format(player.name)
		if len(player.dice) == 0:
			msg += ' {0} is out!'.format(player.name)
			self.first_player = self.get_next_player(player)
			self.players.remove(player)
		elif len(player.dice) == 1 and player.palifico_round == -1:
			player.palifico_round = self.round + 1
			msg += ' Last die! {0} is palifico!'.format(player.name)
		else:
			msg += ' Only {0} left!'.format(len(player.dice))
		print(msg)
		self.total_dice = self.total_dice - 1

	def is_palifico_round(self):
		if len(self.players) < 3:
			return False
		for player in self.players:
			if player.palifico_round == self.round:
				return True
		return False

	def get_next_player(self, player):
		return self.players[(self.players.index(player) + 1) % len(self.players)]

	def get_previous_player(self, player):
		return self.players[(self.players.index(player) - 1) % len(self.players)]