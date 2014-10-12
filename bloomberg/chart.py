from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from API import *
import json
from django.utils.safestring import SafeString

class Organisation():
    def __init__(self, name, ticker, sector, price):
        self.name = name
        self.ticker = ticker
        self.sector = sector
        self.share_price = price

def data_missing(org):
    for entry in ["title", "sector", "price"]:
        if org[entry] == "" or org[entry] == " " or org[entry] == 0:
            return True
    
    return False
    
def lukas_form_to_normal_form(data):
    orgs = []
    
    for key in data.keys():
        org = data[key]
        try:
            if data_missing(org):
                break
                
            orgs.append(Organisation(org["title"], key, org["sector"], org["price"]))
        except:
            pass
    
    return organisations
        
def add_to_json_list(org, data, data_size):
    for entry in data:
        if entry["name"] == org.sector:
            if data_size > 200:
                entry["children"].append({"name": org.ticker, "size": org.share_price})
            else:
                entry["children"].append({"name": org.name, "size": org.share_price})
            return
    
    entry = {"name": org.sector, "children":[{"name":org.name, "size":org.share_price}]}
    data.append(entry)

def generate_json(data):
    output = {"name": "flare", "children": []}
    prices = getCompaniesHistory(get_new_session(), data.keys(), "20141001", "20141031", "MONTHLY")
    
    for price_data in prices:
        data[price_data["ticker"]]["price"] = int(price_data["price"])
        
    organisations = lukas_form_to_normal_form(data)

    data_size = len(data)
    for org in organisations:
        add_to_json_list(org, output["children"], data_size)
    
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

    stock_num = "BP/ LN"
    his = "a"
    ax = "a"
    
    try:
        stock_num = request.GET.get('stock', '')
    except:
        pass
    
    
    
    
    try:
        his = request.GET.get('his', '')
    except:
        pass
            
    try:
        ax = request.GET.get('axis', '')
    except:
        pass
        
    if his == "b":
        hisFile = "Plages.tsv"
    elif his == "c":
        hisFile = "Other.tsv"
    else:
        hisFile = "War.tsv"
        
    if ax == "b":
        axisType = "change"
    elif ax == "c":
        axisType = "volume"
    elif ax == "d":
        axisType = "volitility"
    else:
        axisType = "price"
     
    d = json.dumps(getCompaniesHistory(get_new_session(), [stock_num], 20000101, 20140215, "MONTHLY"))   
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {"stock": stock_num, "his":his, "ax":ax, "file":hisFile, "axisName":axisType, "derData":SafeString(d)}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'chart/historyChart.html', context_dict)
