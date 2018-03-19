from bs4 import BeautifulSoup
import os
import requests
import json

     
def lambda_function(req,context):
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    return res
    

def searchElCorteIngles(product,limit = -1,inbound=0):
    website = 'https://www.elcorteingles.es/electronica/moviles-y-smartphones/'
    query = website + 'search/?s=telefono+' + product
    r = requests.get(query)
    soup = BeautifulSoup(r.content,"html5lib")
    items = soup.find("ul",{"class":"product-list 4"}).find_all("li")
    #speech = "Los {0} Productos mas vendidos son:".format(str(limit) if limit else
    speech= '' 
    for i, item in enumerate(items):
        if (i<inbound):
            continue
        datajson = json.loads(item.find("span")['data-json'])
        name = datajson["name"]
        price = 'a {0} Euros.'.format( datajson["price"]['final']) if "final" in datajson["price"] else ""
        speech = speech + "{0}: {1} {2}.\n ".format(i,name ,price)
        if (i == limit):
            break
    return  { "speech": speech,
              "displayText": speech,
              "source": "apiai-eci"
            }

def makeResponse(req,parameter='item'):      
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get(parameter)
    inbound=parameters.get("inbound") if parameters.get("inbound") else 0
    limit=parameters.get("limit") if parameters.get("limit") else -1
    return searchElCorteIngles(item, limit, inbound)