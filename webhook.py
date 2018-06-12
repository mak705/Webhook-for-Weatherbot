import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print (json.dumps(req, indent=4))
    
    res = makeResponse(req)
    res = json.dumps(res, indent=4) 
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get('parameters')
    city = parameters.get('geo-city')
    date = parameters.get('date')
    r =  request.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=b6907d289e10d714a6e88b30761fae22') 
    json_object = r.json()
    weather = json_object('list')
#   for i in len(weather):
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition = weather[i]['weather'][0]['description']
            break 

#speech: Actual text response to request that fulfilled by server
#display text: shown on device screen
#source: source where we got response
#api.pi> docs > fulfilment > response
    speech = 'The forecast for the'+city+'for the'+date+'is'+condition
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug = False, port=port, host='0.0.0.0')
