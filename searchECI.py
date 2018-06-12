from bs4 import BeautifulSoup
import os
import requests
import json
import filters




def url_filter(product,price_range=[None,None],discount=None,category = 'electronica',subcategory = 'moviles-y-smartphones',helper_search='telefono',page=1,sort_method='bestSellerQtyDesc'):
    """
    crea la url y genera filtros para las opciones indicadas en el json del Post.
    """

    if category not in filters.categories:
        raise ValueError("invalidad category. Check in filters.py or in the website")
    website = 'https://www.elcorteingles.es/{0}/{1}'.format(category,subcategory+'/' if subcategory else '') 
    product=product.lower()
    filters_data=[]
    # en caso de que el usuario quiera un producto en un rango de precio
    ## verifica que el usuario ha metido o precio minimo o maximo
    if any(price_range):
        # mapea con los escritos en filters.prices_mapper
        prices = filters.prices_mapper.keys()
        
        min_price, max_price = price_range
        # en caso de que no establecer maximo o minimo se coge el de filtros maximo o minimo
        max_price = max_price if max_price else max(prices)
        min_price = min_price if min_price else min(prices)
        
        keys = list(map(lambda x: x if ((x >= min_price) & (x<= max_price)) else None,prices))
        prices_filts='price::'+''.join([filters.prices_mapper[key] for key in keys if key])
        
        filters_data.append(prices_filts)
       
    
    # en caso de que el usuario haya pedido con descuentos
    if discount:
        discounts = filters.discounts.keys()
        keys = list(map(lambda x: x if (x >= discount) else None,discounts))
        discount_filts='discount::'+''.join([filters.discounts[key] for key in keys if key])
        
        filters_data.append(discount_filts)

    # en caso de estar nuestro producto (ej samsung) en nuestro filters.brands, lo utiliza para filtrar
    # en caso contrario (else), hace una busqueda generica 
    if product in list(map( lambda x: x.lower() , filters.brands.keys())):
        filters_data.append(filters.brands[product])
        query = website + '/{0}/?f='.format(page)+ '||'.join(map(str,filters_data)) + '&s={0}'.format(category)
    else:
        if filters_data:     
            query = website + 'search/{0}/?s={1}+'.format(page,helper_search) + product + '&f='+ '||'.join(map(str,filters_data))
        else:
            query = website + 'search/{0}/?s={1}+'.format(page,helper_search) + product
    if (sort_method in ['newInAsc','bestSellerQtyDesc','priceAsc','priceDesc','nameAsc','discountPerDesc','stockDesc']):
        query = '{0}&sorting={1}'.format(query,sort_method)    
    return query 


def request_el_corte_ingles(product,price_min=None,price_max=None,discount=None,inumber = -1,limit=0,init_item=0,category = 'electronica',subcategory = 'moviles-y-smartphones',helper_search='telefono',page=1,sort_method='bestSellerQtyDesc'):
    """
    extrae los items de una URL del corte ingles generada con los filtros de la función url_filter.
    """
    query = url_filter(product,price_range=[price_min,price_max],discount=discount,category=category,subcategory=subcategory,helper_search=helper_search,page=page,sort_method=sort_method)
    print(query)
    r = requests.get(query)
    soup = BeautifulSoup(r.content,"html5lib")
    # buscamos la lista de productos que se muestra en la web (he visto dos casos de clases que los contiene
    # product-list 4 (en smatphones) y product-list (en ropa)
    items = soup.find("ul",{"class":"product-list 4"}) if soup.find("ul",{"class":"product-list 4"}) else soup.find("ul",{"class":"product-list"})
    # si no encuentra items, devuelve items=[]
    if not items: 
       items=[]
    else:   
        items = items.find_all("li")
    items_parsed=[] 
    for i, item in enumerate(items):
        dt= item.find("span")
        if dt:
            datajson = json.loads(dt['data-json'])
        else:
            continue
        
        # extraemos datos por item que vamos a meter en el JSON de respuesta
        name = datajson["name"]
        img_href= "https:"+item.find("img")['src']
        id_ref=item.find("img")["id"].split('-')[1]       
        href = 'https://www.elcorteingles.es'+item.find('a',{'data-event':"product_click"})['href']
        price =datajson["price"]['final'] if "final" in datajson["price"] else None
        if not price:
            try:
                price_original=item.find("div",{"class":"product-preview "}).find('div',{"class":'info'})
                price_original=price_original.find("div",{"class":"product-price product-price-marketplace marketplace"})
                price_original = price_original.find("span",{"class":"current sale"}) if price_original.find("span",{"class":"current sale"}) else price_original.find("span",{"class":"current "})
                price=price_original.text
            except:
                pass
        discount=int(item.find('span',{'class':'discount'}).text.replace("%","")) if item.find('span',{'class':'discount'})  else None
        item_json={'name':name,'image':img_href,'price':price,'index':i,'discount':discount,'href':href,'id':id_ref}
        #items_parsed.append("{0}: {1} {2} ".format(i,name ,price))
        items_parsed.append(item_json)
    # en caso de haberle puesto un elemento determinado de la lista de productos, devolvemos ese
    # si hemos puesto limite idem
    if inumber>=0:
        items_parsed=[items_parsed[inumber]]        
    elif limit>0:
        items_parsed=items_parsed[init_item:(init_item+limit)]
    
        
    return items_parsed


  

def response_db(req,parameter='item'):   
    """
    Respuesta generada a partir del request (JSON de entrada). Los posibles parametros de JSON de entrada son:
    inumber: si hemos con anterioridad mirado una lista de items y queremos el número inumber
    limit: número maximo de elementos representados
    price_min: precio mínimo del producto
    price_max: precio máximo del producto
    discount: mínimo descuento con el que queremos ver el producto (en fase alpha, en pruebas)
    """   
    #Extraemos parametros posibles del JSON de entrada
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get(parameter)
    inumber=parameters.get("inumber") if parameters.get("inumber") else -1
    limit=parameters.get("limit") if parameters.get("limit") else -1
    price_min=parameters.get("price_min") if parameters.get("price_min") else None
    price_max=parameters.get("price_max") if parameters.get("price_max") else None
    discount=parameters.get("discount") if parameters.get("discount") else None
    category=parameters.get("category") if parameters.get("category") is not None else 'electronica'
    subcategory=parameters.get("subcategory") if parameters.get("subcategory") is not None else 'moviles-y-smartphones'
    helper_search=parameters.get("helper_search") if parameters.get("helper_search") is not None else 'telefono'
    page=parameters.get("page") if parameters.get("page") else 1
    init_item=parameters.get("init_item") if parameters.get("init_item") else 0
    sort_method=parameters.get("sort_method") if parameters.get("sort_method") else 'bestSellerQtyDesc'

    # A partir de estos parametros generamos el JSON de salida
    items_parsed = request_el_corte_ingles(item,price_min=price_min,price_max=price_max,discount=discount,inumber = inumber,init_item=init_item,limit=limit,category=category,subcategory=subcategory,helper_search=helper_search,page=page,sort_method=sort_method)
    return items_parsed


def request_item_url(url):
    """
    Extracción de entidades a partir de la url de un producto. 
    """
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html5lib")
    # buscamos en features caracteristicas e informacion del producto
    features = soup.find("div",{"id":"features"})
    item_name = soup.find('div',{'id':'product-info'}).find('h2',{'class':'title'}).text.strip()
    sku = soup.find('div',{'id':'product-info'}).find("span",{"id":"sku-ref"}).text.strip()
    description=features.find('div',{'id':'description'})
    description=description.text if description else "No disponible" # por si acaso no hay disponible descripcion
    price = soup.find('span',{'class':'current sale'}) if soup.find('span',{'class':'current sale'}) else soup.find('span',{'class':'current'})
    price=price.text if price else "No disponible" # por si acaso no hay disponible precio
    img = 'https:'+soup.find('img',{'id':'product-image-placer'})['src']
    features_esp = soup.find("div",{"class":"product-features c12"}) # textraccion de caracteristicas del item
    features_key = features_esp.find_all('dt')
    features_value = features_esp.find_all('dd')
    features_dict = {k.text:v.text for k,v in zip(features_key,features_value)}
    return {'name': item_name,
            'description':description,
            'price':price,
            'img':img,
            'href':url,
            'sku':sku,
            'features':features_dict,
            
    }


def response_db_item(req,parameter='item'):     
    """
    extraemos los parámetros del request a partir de la url del producto. El JSON de entrada tiene la forma:
    href: url del item
    el json de salida tiene la forma descripta en la función request_item_url()
    """ 
    result = req.get("result")
    parameters = result.get("parameters")
    
    url = parameters.get("href") if parameters.get("href") else None
        
    # extraccion de los datos del producto con la url
    items_parsed = request_item_url(url)
    return items_parsed





def request_el_corte_ingles_as_DialogFlow_json(items_parsed):
    """
    devuelve el speech reconocido por DialogFlow.
    """
    items=[ '{0}:{1} a {2}.'.format(item['index'],item['name'], '{0} Euros'.format(item['price']) if item['price'] else  "NA") for item in items_parsed]
    speech = '\n '.join(items)
    return  { "speech": speech,
              "displayText": speech,
              "source": "apiai-eci"
            }


def response_webhook(req,parameter='item'): 
    """
    respuesta para DialogFlow
    """     
    items_parsed = response_db(req,parameter=parameter)
    return request_el_corte_ingles_as_DialogFlow_json(items_parsed)




def lambda_function_multipleItems(req,context):
    """
    funcion lambda para levantar la búsqueda de múltiples Items en AWS lambda.
    """
    req = request.get_json(silent=True, force=True)
    res = response_webhook(req)
    res = json.dumps(res, indent=4)
    return res
