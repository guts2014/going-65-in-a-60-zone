# Abstraction layer over Bloomberg API

import blpapi

PX_LAST = "PX_LAST"
GICS_SECTOR_NAME = "GICS_SECTOR_NAME"
TITLE = "DS002"
DATE = "date"

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
def _getData(session, requestName, securities, givenFields, start=None, end=None, periodicity=None):
    session.openService("//blp/refdata")
    refDataService = session.getService("//blp/refdata")
    request = refDataService.createRequest(requestName)
    for security in securities:
        request.append("securities", security)
    for field in givenFields:
        request.append("fields", field)
    if requestName == "HistoricalDataRequest":
        request.set("periodicitySelection", periodicity)
        request.set("startDate", start)
        request.set("endDate", end)
    session.sendRequest(request)
    results = {}
    if requestName == "ReferenceDataRequest":
        while(True):
            # We provide timeout to give the chance to Ctrl+C handling:
            event = session.nextEvent(500)
            for msg in event:
                if msg.messageType() == "ReferenceDataResponse":
                    securityData = msg.getElement("securityData")
                    for field in securityData.values():
                        fieldData = field.getElement("fieldData")
                        if fieldData.hasElement("INDX_MEMBERS"):
                            indxMembers = fieldData.getElement("INDX_MEMBERS")
                            names = []
                            for member in indxMembers.values():
                                name = member.getElement("Member Ticker and Exchange Code").getValue()
                                names += [name + " Index"]
                            results = _getData(session, requestName, names, [GICS_SECTOR_NAME, TITLE])
                        else:
                            result = {}
                            for name in givenFields:
                                if fieldData.hasElement(GICS_SECTOR_NAME) and name == GICS_SECTOR_NAME:
                                    result["sector"] = fieldData.getElementAsString(blpapi.Name(name))
                                elif fieldData.hasElement(TITLE) and name == TITLE:
                                    result["title"] = fieldData.getElementAsString(blpapi.Name(name))
                            ticker = field.getElementAsString("security").replace(" Index", "")
                            results[ticker] = result
                 
            if event.eventType() == blpapi.Event.RESPONSE:
                break
    elif requestName == "HistoricalDataRequest":
        results = []
        while(True):
           event = session.nextEvent(500)
           for msg in event:
               if msg.messageType() == "HistoricalDataResponse":
                   securityData = msg.getElement("securityData")
                   fieldData = securityData.getElement("fieldData")
                   for field in fieldData.values():
                       result = {}
                       if field.hasElement(PX_LAST):
                               result["price"] = field.getElementAsFloat(PX_LAST)
                       if field.hasElement(DATE):
                               result["date"] = field.getElementAsString(DATE)
                       result["ticker"] = securityData.getElementAsString("security").replace(" Index", "")
                       results += [result]
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
# AAL LN is a ticker
#Returns { "AAL LN": { "title": "Amazon", "sector": "Education" }
def getAllCompaniesList(session):
    return _getData(session, "ReferenceDataRequest", ["UKX Index", "SPX Index"], ["INDX_MEMBERS"])

def getCompaniesHistory(session, companies, start, end, periodicity):
    return _getData(session, "HistoricalDataRequest", [s + " Index" for s in companies], [PX_LAST], start, end, periodicity)
