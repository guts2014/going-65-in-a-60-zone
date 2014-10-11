import json

def get_company_share_price(company, date):
    pass

def generate_json(companies, dates):
    data = {}
    
    for date in dates:
        date_data = {}
        
        for company in company:
            date_data["name"] = company
            date_data["price"] = get_company_share_price(company)
        
        data[date] = date_data
    
    return json.dumps(data)