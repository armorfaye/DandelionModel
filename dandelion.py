from decimal import Decimal, getcontext
import numpy as np
import random

class Dandelion:
	def __init__(self, position, mature, lastlanding):
		self.position = position  # Now a tuple
		self.mature = mature
		self.lastlanding = lastlanding

	def isMature(self, day, growth_time):
		self.mature = ((day - self.lastlanding) >= growth_time)

	def ifGerminate(self, probability):
		return random.random() < probability

	def simulate(self, wind, time_to_land):
		pos_x, pos_y = self.position
		for _ in range(int(time_to_land)):
			wind.add_noise()
			pos_x += Decimal(str(wind.speed)) * Decimal(str(np.cos(wind.direction))) 
			pos_y += Decimal(str(wind.speed)) * Decimal(str(np.sin(wind.direction))) 
		wind.add_noise()
		pos_x += Decimal(str(wind.speed)) * Decimal(str(np.cos(wind.direction))) * (time_to_land % Decimal('1'))
		pos_y += Decimal(str(wind.speed)) * Decimal(str(np.sin(wind.direction))) * (time_to_land % Decimal('1'))
		self.position = (pos_x, pos_y)
