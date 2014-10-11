from bloomberg import *
from django.http import HttpResponse

def connection_status(request):
    if get_new_session() == None:
        return HttpResponse("Unable to connect to Bloomberg database")
    
    return HttpResponse("Successfully connected to Bloomberg database")