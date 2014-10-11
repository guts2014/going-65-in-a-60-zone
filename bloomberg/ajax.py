import json

# Convert DD/MM/YYYY into a number for comparison
def date_to_number(date):
    date_parts = date.split("/")
    number_string = date_parts[2] + date_parts[1] + date_parts[0]
    return int(number_string)

def get_company_share_price(company, date):
    pass

def generate_json(companies, start_date, end_date):
    start = date_to_number(start_date)
    end = date_to_number(end_date)
    
    data = {}
    
    for date in dates:
        date_data = {}
        
        for company in company:
            date_data["name"] = company
            date_data["price"] = get_company_share_price(company)
        
        data[date] = date_data
    
    return json.dumps(data)