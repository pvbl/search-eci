from bs4 import BeautifulSoup
import os
import requests
import json
import filters
     
def lambda_function(req,context):
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    return res
    

def url_filter(product,product_filters):
    website = 'https://www.elcorteingles.es/electronica/moviles-y-smartphones/' 
    product=product.lower()
    
    if product in list(map( lambda x: x.lower(),filters.brands.keys())):
		query = website + 'search/?f='+ filters.brands['product']
	    
	else:	 
        query = website + 'search/?s=telefono+' + product
    if product_filters:
		
    
     		
	
	url = query + '&s=electronica'
    return url 

def searchElCorteIngles(product,product_pricefilters=[],product_discountfilters=[],inumber = -1,limit=0):
    query = url_filter(product,product_filters)
    
    r = requests.get(query)
    soup = BeautifulSoup(r.content,"html5lib")
    items = soup.find("ul",{"class":"product-list 4"}).find_all("li")
    #speech = "Los {0} Productos mas vendidos son:".format(str(limit) if limit else
    items_parsed=[] 
    for i, item in enumerate(items):
        datajson = json.loads(item.find("span")['data-json'])
        name = datajson["name"]
        href= item.find("img")['src']
        price = 'a {0} Euros.'.format( datajson["price"]['final']) if "final" in datajson["price"] else ""
        items_parsed.append("{0}: {1} {2} ".format(i,name ,price))
    if inumber>=0:
		items_parsed=[items_parsed[inumber]]
	elif limit>0:
		items_parsed=items_parsed[:limit]
	
    speech = '.\n'.join(items_parsed)
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
