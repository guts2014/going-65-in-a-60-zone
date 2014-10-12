from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from sound_mixer import SoundMixer
from API import *

def sounds_page(request):
	session = get_new_session()
	
	# BP
	historical_data = getCompaniesHistory(session, ['BP/ LN'], 20120101, 20140101, 'MONTHLY')
	
	historical_prices = []
	for dict in historical_data:
		historical_prices.append(dict['price'])
	
	mixer = SoundMixer()
	mixer.add_dataset(historical_prices)
	mixer.generate_file('stock1')
	
	# RDSB
	historical_data = getCompaniesHistory(session, ['RDSB LN'], 20120101, 20140101, 'MONTHLY')
	
	historical_prices = []
	for dict in historical_data:
		historical_prices.append(dict['price'])
	
	mixer = SoundMixer()
	mixer.add_dataset(historical_prices, 400)
	mixer.generate_file('stock2')
	
	return render(request, "sounds.html")