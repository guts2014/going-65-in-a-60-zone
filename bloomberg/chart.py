from django.shortcuts import render
from django.http import HttpResponse
from bloomberg import *
import json

class Organisation():
    def __init__(self, name, sector, price):
        self.name = name
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
                
            organisations.append(Organisation(org["title"], org["sector"], 10))
        except:
            pass
    
    return organisations
        
def add_to_json_list(org, data):
    for entry in data:
        if entry["name"] == org.sector:
            entry["children"].append({"name": org.name, "size": org.share_price})
            return
    
    entry = {"name": org.sector, "children":[{"name":org.name, "size":org.share_price}]}
    data.append(entry)

def generate_json():
    output = {"name": "flare", "children": []}
    data = getAllCompaniesList(get_new_session())
    print(data)
    organisations = lukas_form_to_normal_form(data)
    print("Done getting data")

    for org in organisations:
        add_to_json_list(org, output["children"])
    
    return output

def zoom_circles_page(request):
    return render(request, "chart/zoomable-circle-packaging.html", {})
    
def zoom_circles_data(request):
    print("Starting to get data")
    return HttpResponse(json.dumps(generate_json()))