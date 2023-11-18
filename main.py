import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
import pandas as pd
from scipy.interpolate import interp1d
from wind import Wind
from dandelion import Dandelion

# Constants and Parameters
g = Decimal('9.81')
seed_mass_range = (0.34, 0.54)
field_size = (-50, 50)
getcontext().prec = 25
updraft_height_mean = Decimal('0.2')
num_days = 50
growth_time = 30

# Load and Interpolate Data
df = pd.read_csv('germination_probability.csv')
df.columns =  ['Day', 'Probability']

# Initialize Wind
wind = Wind('WindData.csv')

# Utility Functions
def calculate_landing_time(seed_mass, g):
	terminal_velocity = (Decimal('1') / Decimal('16')) * (100 * Decimal(seed_mass) * g) ** (Decimal('1') / Decimal('2'))
	updraft_height = Decimal(str(np.random.normal(float(updraft_height_mean), 0.1))) + Decimal('0.1') 
	return updraft_height / terminal_velocity

def calculate_NS(coefficients, values):
	return np.dot(coefficients, values)

# Simulation
dandelions = [Dandelion((Decimal('0'), Decimal('0')), True, 0)]
coefficients = np.array([0.077, 0.063, 0.498])
for day in range(num_days):
	values = np.array([12.55 * np.sin(0.016 * day - 1.58) + 12.27, 4.98 * np.sin(1.01 * day - 0.22) + 9.31, -2.62 * np.sin(0.02 * day + 1.86) + 12.10])
	#number_of_seeds = calculate_NS(coefficients, values)
	number_of_seeds = 200
	new_dandelions = []
	for dandelion in dandelions:
		wind.generate_wind(day)
		if dandelion.mature:
			for _ in range(int(number_of_seeds)):
				seed_mass = np.random.uniform(*seed_mass_range)
				time_to_land = calculate_landing_time(seed_mass / 1000, g)
				new_position = list(dandelion.position)
				new_dandelion = Dandelion(tuple(new_position), False, day)
				if new_dandelion.ifGerminate(df['Probability'][day]):
					new_dandelion.simulate(wind, time_to_land)
					new_dandelions.append(new_dandelion)
				wind.generate_wind(day)
		else: 
			dandelion.isMature(day, growth_time)
	dandelions.extend(new_dandelions)

all_positions = [list(map(float, d.position)) for d in dandelions]

# Plotting
plt.figure(figsize=(10, 8))
plt.scatter(*zip(*all_positions), alpha=0.6, color='green')   # Using green to represent all dandelions
plt.xlim(field_size[0], field_size[1])
plt.ylim(field_size[0], field_size[1])
plt.title('All Dandelion Positions')
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.grid(True)
plt.show()
