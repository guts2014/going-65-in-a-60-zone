# Abstraction layer over Bloomberg API

import blpapi

def get_new_session():
    session_options = blpapi.SessionOptions()
    session_options.setServerHost("10.8.8.1")
    session_options.setServerPort(8194)
    
    print("Connecting to Bloomberg server")
    session = blpapi.Session(session_options)
    
    if not session.start():
        return None
    
    return session

def session_market_data(session, requests):
    if not session.openService("//blp/mktdata"):
        print("Unable to connect to Market Data on Bloomberg")
        return None
        
    subscriptions = blpapi.SubscriptionList()
    subscriptions.add(requests)
    session.subscribe(subscriptions)
    return session

# Do not use
"""    
def session_reference_data(session):
    if not session.openService("//blp/refdata"):
        print("Unable to connect to Reference Data on Bloomberg")
        return None
    
    data_service = session.getService("//blp/refdata")
    request = data_service.createRequest("HistoricalDataRequest")
"""