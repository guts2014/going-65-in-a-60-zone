#!/usr/bin/env python
from wavebender import *
from itertools import *
import sys

class SoundMixer:

	dataset_limit = 5

	base_frequencies = [1000, 400, 700, 1000, 1300]
	wave_lengths = [0.8, 0.8, 0.8, 0.8, 0.8]
	frequency_step = 200

	def __init__(self):
		self.datasets = [] # list of 1-dimensional datasets
		self.frequencies = []
		
	# Interface
		
	def add_dataset(self, data, frequency=None):
	
		if(len(self.datasets) < SoundMixer.dataset_limit):
			self.datasets.append(data)
			if frequency == None:
				frequency = SoundMixer.base_frequencies[len(self.datasets) - 1]
			self.frequencies.append(self.generate_frequencies_list(data, frequency))
		
	def generate_file(self, filename):
		channel_data = self.generate_channel_data()
		channels = (channel_data, channel_data)
		samples = compute_samples(channels, None)
		write_wavefile('static/sounds/' + filename + '.wav', samples, None)
		
	# Helper methods
		
	def generate_channel_data(self):
		channel_data = []
	
		for i in range(len(self.datasets)):
			channel_data.append(self.generate_waves_for_dataset(i))
	
		return channel_data
		
	def generate_waves_for_dataset(self, dataset_index):
		waves = []
		for frequency in self.frequencies[dataset_index]:
			waves.append(self.generate_islice_wave(frequency, SoundMixer.wave_lengths[dataset_index]))
			#pause
			#waves.append(self.generate_islice_wave(0.0, 0.1))
			
		return chain.from_iterable(waves)
		
	def generate_islice_wave(self, frequency, length):
		l = int(44100 * length)	
		print frequency
		return islice(damped_wave(frequency=frequency, amplitude=0.1, length=int(l/4)), l)
		
	def generate_frequencies_list(self, dataset, base_frequency):
		frequencies = []
		prev = None
		current_frequency = base_frequency
		
		for value in dataset:
			if prev != None and value > prev:
				current_frequency += SoundMixer.frequency_step
			elif prev != None and value < prev:
				current_frequency -= SoundMixer.frequency_step
				
			frequencies.append(current_frequency)
			prev = value
		
		return frequencies