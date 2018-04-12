import json
import os
import searchECI


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    webhook para consumir desde Dialogflow
    """
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = searchECI.response_webhook(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

@app.route('/searcheci', methods=['POST'])
def search_eci():
    """
    ruta para que devuelva una lista de items a partir de unos parametros determinados como JSON.
    """
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = searchECI.response_db(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/returnItem', methods=['POST'])
def return_item():
    """
    ruta para la devolucion de información de un item concreto como JSON.
    """
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = searchECI.response_db_item(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')


