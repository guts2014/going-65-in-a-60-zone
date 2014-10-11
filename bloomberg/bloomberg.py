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

def session_subscribe(session, requests):
    session.openService("//blp/mktdata")
    subscriptions = blpapi.SubscriptionList()
    subscriptions.add(requests)
    session.subscribe(subscriptions)
    return session