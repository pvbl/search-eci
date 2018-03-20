from bs4 import BeautifulSoup
import os
import requests
import json
import filters
     
def lambda_function(req,context):
    """
    funcion lambda para su uso en AWS lambda
    """
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    return res
  


def url_filter(product,price_range=[None,None],discount=None):
    website = 'https://www.elcorteingles.es/electronica/moviles-y-smartphones/' 
    product=product.lower()
    filters_data=[]
    # en caso de que el usuario quiera un producto en un rango de precio
    if any(price_range):
        prices = filters.prices_mapper.keys()
        
        min_price, max_price = price_range
        max_price = max_price if max_price else max(filters.prices_mapper.keys())
        min_price = min_price if min_price else min(filters.prices_mapper.keys())
        keys = list(map(lambda x: x if ((x >= min_price) & (x<= max_price)) else None,prices))
        _ = [filters_data.append(filters.prices_mapper[key]) for key in keys if key]
    
    # en caso de que el usuario haya pedido con descuentos
    if ((discount!=None) & (discount in filters.discounts)):
        filters_data.append(filters.discounts[discount])


    if product in list(map( lambda x: x.lower(),filters.brands.keys())):
        filters_data.append(filters.brands[product])
        query = website + '?f='+ ','.join(map(str,filters_data)) + '&s=electronica'
        
    else:
        if filters_data:     
            query = website + 'search/?s=telefono+' + product + '?f='+ ','.join(map(str,filters_data))
        else:
            query = website + 'search/?s=telefono+' + product
                 
 
    return query 


def request_el_corte_ingles(product,price_min=None,price_max=None,discount=None,inumber = -1,limit=0):
    query = url_filter(product,price_range=[price_min,price_max],discount=discount)
    
    r = requests.get(query)
    soup = BeautifulSoup(r.content,"html5lib")
    items = soup.find("ul",{"class":"product-list 4"})
    if not items:
        items=[]
    else:   
        items = items.find_all("li")
    #speech = "Los {0} Productos mas vendidos son:".format(str(limit) if limit else
    items_parsed=[] 
    for i, item in enumerate(items):
        datajson = json.loads(item.find("span")['data-json'])
        name = datajson["name"]
        href= item.find("img")['src']
        price = 'a {0} Euros.'.format( datajson["price"]['final']) if "final" in datajson["price"] else ""
        item_json={'name':name,'url':href,'price':price,'index':i}
        #items_parsed.append("{0}: {1} {2} ".format(i,name ,price))
        items_parsed.append(item_json)
    if inumber>=0:
        items_parsed=[items_parsed[inumber]]
    elif limit>0:
        items_parsed=items_parsed[:limit]
    return items_parsed
    

def request_el_corte_ingles_as_json(items_parsed):
    return json.dumps(items_parsed)    

def request_el_corte_ingles_as_DialogFlow_json(items_parsed):
    
    items=[ '{0}:{1} a {2}\n'.format(item['index'],item['name'],item['price']) for item in items_parsed]
    speech = '.\n'.join(items)
    return  { "speech": speech,
              "displayText": speech,
              "source": "apiai-eci"
            }

def response_webhook(req,parameter='item'):      
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get(parameter)
    inumber=parameters.get("inumber") if parameters.get("inumber") else 0
    limit=parameters.get("limit") if parameters.get("limit") else -1
    price_min=parameters.get("price_min") if parameters.get("price_min") else None
    price_max=parameters.get("price_max") if parameters.get("price_max") else None
    discount=parameters.get("discount") if parameters.get("discount") else None
    items_parsed = request_el_corte_ingles(item,price_min=price_min,price_max=price_max,discount=discount,inumber = -1,limit=0)
    return request_el_corte_ingles_as_DialogFlow_json(items_parsed)
