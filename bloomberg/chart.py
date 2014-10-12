from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from API import *
import json

class Organisation():
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.share_price = price
        

def lukas_form_to_normal_form(data):
    organisations = []
    
    for key in data.keys():
        org = data[key]
        try:
            if org["title"] == "" or org["title"] == " ":
                break
                
            if org["sector"] == "" or org["sector"] == " ":
                break
                
            if org["price"] == "" or org["price"] == 0:
                break
                
            organisations.append(Organisation(org["title"], key, org["sector"], org["price"]))
        except:
            pass
    
    return organisations
        
def add_to_json_list(org, data):
    for entry in data:
        if entry["name"] == org.sector:
            entry["children"].append({"name": org.ticker, "size": org.share_price})
            return
    
    entry = {"name": org.sector, "children":[{"name":org.name, "size":org.share_price}]}
    data.append(entry)

def generate_json(data):
    output = {"name": "flare", "children": []}
    prices = getCompaniesHistory(get_new_session(), data.keys(), "20141001", "20141031", "MONTHLY")
    
    for price_data in prices:
        data[price_data["ticker"]]["price"] = int(price_data["price"])
        
    organisations = lukas_form_to_normal_form(data)
    print("Done getting data")

    for org in organisations:
        add_to_json_list(org, output["children"])
    
    return output

def zoom_circles_page(request, country):
    return render(request, "chart/zoomable-circle-packaging.html", {"country": country})
    
def zoom_circles_data(request, country):
    if country == "UK":
        data = generate_json(getUKCompaniesList(get_new_session()))
    else:
        data = generate_json(getUSCompaniesList(get_new_session()))
        
    return HttpResponse(json.dumps(data))
    
def history(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'chart/historyChart.html', context_dict)
