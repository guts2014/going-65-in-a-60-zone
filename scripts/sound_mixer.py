#!/usr/bin/env python
from wavebender import *
from itertools import *
import sys

class SoundMixer:

	dataset_limit = 5

	base_frequencies = [100, 400, 700, 1000, 1300]
	wave_lengths = [0.16, 0.16, 0.16, 0.16, 0.16]
	frequency_step = 100

	def __init__(self):
		self.datasets = [] # list of 1-dimensional datasets
		self.frequencies = []
		
	# Interface
		
	def add_dataset(self, data):
		if(len(self.datasets) < SoundMixer.dataset_limit):
			self.datasets.append(data)
			self.frequencies.append(self.generate_frequencies_list(data, SoundMixer.base_frequencies[len(self.datasets) - 1]))
		
	def generate_file(self):
		channel_data = self.generate_channel_data()
		channels = (channel_data, channel_data)
		samples = compute_samples(channels, None)
		write_wavefile('out.wav', samples, None)
		
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
			
		return chain.from_iterable(waves)
		
	def generate_islice_wave(self, frequency, length):
		l = int(44100 * length)	
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

''''		
ibm = [184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900]
other = [44, 88, 99, 31, 30, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 3144, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31, 30, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 3144, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31]
asd = [184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900, 184.7700, 182.8800, 177.1200, 187.2600, 177.1400, 186.3900]
sad = [44, 88, 99, 31, 30, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 3144, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31, 30, 44, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 3144, 88, 99, 31, 44, 88, 99, 31, 44, 88, 99, 31]


mixer = SoundMixer()
mixer.add_dataset(ibm)
mixer.add_dataset(other)
mixer.add_dataset(asd)
mixer.add_dataset(sad)

mixer.generate_file()
''''