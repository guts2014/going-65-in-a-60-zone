# Abstraction layer over Bloomberg API

import blpapi

PX_LAST = "PX_LAST"
GICS_SECTOR_NAME = "GICS_SECTOR_NAME"
TITLE = "DS002"

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

#results[field.getElementAsFloat(blpapi.Name("PX_LAST"))]
def _getData(session, requestName, securities, givenFields):
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest(requestName)
    for security in securities:
        request.append("securities", security)
    for field in givenFields:
        request.append("fields", field)
    session.sendRequest(request)
    
    counter = 0
    results = {}
    while(True):
        counter += 1
        print("Started an iteration" + str(counter))
        # We provide timeout to give the chance to Ctrl+C handling:
        event = session.nextEvent(500)
        for msg in event:
            if msg.messageType() == "ReferenceDataResponse":
                securityData = msg.getElement("securityData")
                for field in securityData.values():
                    field = field.getElement("fieldData")
                    if field.hasElement("INDX_MEMBERS"):
                        indxMembers = field.getElement("INDX_MEMBERS")
                        for member in indxMembers.values():
                            name = member.getElement("Member Ticker and Exchange Code").getValue()
                            results[name] = _getData(session, requestName, [name + " Index"], [GICS_SECTOR_NAME, TITLE])
                            print(len(results))
                    else:
                        result = {}
                        for name in givenFields:
                            if field.hasElement(GICS_SECTOR_NAME) and name == GICS_SECTOR_NAME:
                                result["sector"] = field.getElementAsString(blpapi.Name(name))
                            elif field.hasElement(TITLE) and name == TITLE:
                                result["title"] = field.getElementAsString(blpapi.Name(name))
                        return result
                 
        if event.eventType() == blpapi.Event.RESPONSE:
            break

    return results

#Get TOP 100 UK
def getUKCompaniesList(session):
    return _getData(session, "ReferenceDataRequest", ["UKX Index"], ["INDX_MEMBERS"])

#Top 500 US companies list of indices
def getUSCompaniesList(session):
    return _getData(session, "ReferenceDataRequest", ["SPX Index"], ["INDX_MEMBERS"])

#Get all 600 companies list US and UK
def getAllCompaniesList(session):
    return _getData(session, "ReferenceDataRequest", ["UKX Index", "SPX Index"], ["INDX_MEMBERS"])