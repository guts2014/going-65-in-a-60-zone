from bloomberg import *
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

def connection_status(request):
	if get_new_session() == None:
		return HttpResponse("Unable to connect to Bloomberg database")
	
	return HttpResponse("Successfully connected to Bloomberg database")
	
	
def main(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	
	stock_num = request.GET.get('stock', '')
	
	# Construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template!
	context_dict = {'lol':stock_num}
	
	print(stock_num)
	
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render(request, 'MainPage.html', context_dict)
