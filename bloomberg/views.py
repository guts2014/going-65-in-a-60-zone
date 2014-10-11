from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from API import getUKCompaniesList, get_new_session
from models import Company


def connection_status(request):
    session = get_new_session()
    # results = getUKCompaniesList(session)
    # for key in results:
    #     current = results[key]
    #     title = ""
    #     sector = ""
    #     if "title" in current:
    #         title = current['title']
    #     if "sector" in current:
    #         sector = current['sector']
    #     new_record = Company(title=title, sector=sector, key=key)
    #     new_record.save()
    print(Company.objects.all())

    if session == None:
        return HttpResponse("Unable to connect to Bloomberg database")
    return HttpResponse("Successfully connected to Bloomberg database")


def main(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    stock_num = request.GET.get('stock', '')
    
    #data = get_stock_data(stock_num);
    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'dataStuff': stock_num}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'MainPage.html', context_dict)


def sector(request, sector_type):
    return render(request, 'ChartView.html', {"type": sector_type})
