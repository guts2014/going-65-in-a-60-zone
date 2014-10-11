from django.shortcuts import render
from django.http import HttpResponse
import json

class Organisation():
    def __init__(self, name, sector, price):
        self.name = name
        self.sector = sector
        self.share_price = price

def add_to_json_list(org, data):
    for entry in data:
        if entry["name"] == org.sector:
            entry["children"].append({"name": org.name, "size": org.share_price})
            return
    
    entry = {"name": org.sector, "children":[{"name":org.name, "size":org.share_price}]}
    data.append(entry)

def generate_json(organisations):
    output = {"name": "flare", "children": []}

    for org in organisations:
        add_to_json_list(org, output["children"])
    
    return output

def zoom_circles_page(request):
    return render(request, "chart/zoomable-circle-packaging.html", {})
    
def zoom_circles_data(request):
    org1 = Organisation("Admiral", "Insurance", "131")
    org2 = Organisation("Esure", "Insurance", "151")
    org3 = Organisation("Sheila's Wheels", "Insurance", "101")
    org4 = Organisation("Direct Line", "Insurance", "171")
    
    org5 = Organisation("Microsoft", "Electronics", "201")
    org6 = Organisation("Apple", "Electronics", "401")
    org7 = Organisation("Google", "Electronics", "331")
    org8 = Organisation("Samsung", "Electronics", "350")
    
    org9  = Organisation("Asda", "Retail", "101")
    org10 = Organisation("Tesco", "Retail", "90")
    org11 = Organisation("Waitrose", "Retail", "89")
    
    orgs = [org1, org2, org3, org4, org5, org6, org7, org8, org9, org10, org11]
    return HttpResponse(json.dumps(generate_json(orgs)))