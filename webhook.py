import json
import os
import requests
from bs4 import BeautifulSoup


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

       
def lambda_function(req,context):
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    return res
    

def searchElCorteIngles(product,limit = None):
    website = 'https://www.elcorteingles.es/'
    query = website + 'search/?s=' + product
    r = requests.get(query)
    soup = BeautifulSoup(r.content,"html5lib")
    items = soup.find("ul",{"class":"product-list 4"}).find_all("li")
    speech = "Los {0} Productos mas vendidos son:".format(str(limit) if limit else "")
    for i, item in enumerate(items):
        datajson = json.loads(item.find("span")['data-json'])
        name = datajson["name"]
        price = datajson["price"]['final'] if "final" in datajson["price"] else "desconodido"
        speech = speech + "{0}: {1} a {2} euros.\n ".format(i,name ,price)
        if (limit!=None) & (i == limit):
            break
    return  { "speech": speech,
              "displayText": speech,
              "source": "apiai-weather-webhook"
            }

def makeResponse(req,parameter='item'):      
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get(parameter)
    return searchElCorteIngles(item)




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')





















