import numpy as np
import pandas as pd


class Wind:
	def __init__(self, wind_data_csv):
		self.wind_df = pd.read_csv(wind_data_csv)
		self.wind_df.columns =  ['Speed', 'Direction']
		self.speed = 0
		self.direction = 0
		self.wind_speed_std = np.std(self.wind_df['Speed'])
		self.wind_direction_std = np.std(self.wind_df['Direction'])

	def generate_wind(self, day):
		self.speed =  np.random.normal(self.wind_df['Speed'][day], self.wind_speed_std)
		self.direction = np.radians(np.random.normal(self.wind_df['Direction'][day], self.wind_direction_std))
	
	def add_noise(self):
		self.speed += np.random.normal(0, 0.1)
		self.direction += np.radians(np.random.normal(0, 3))