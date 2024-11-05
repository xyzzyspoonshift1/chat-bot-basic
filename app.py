from flask import Flask, request,jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    source_amount = data['queryResult']['parameters']['unit-currency']['amount']
    final_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency,final_currency)
    if cf:
        converted_amount = round((source_amount * cf),2)
    else:
        return "Error in fetching conversion factor"
    response ={
        'fulfillmentText' : f"{source_amount} {source_currency} is {converted_amount} {final_currency}"
    }
    return jsonify(response)

def fetch_conversion_factor(source,final):
    url = 'https://api.currencyapi.com/v3/latest?base_currency={}&currencies={}&apikey=cur_live_9wgQ4u4NxQ6m52UtaJvkzq6bIc95xMeXfrUd7Wg6'.format(source,final)
    try:
        response = requests.get(url).json()
        return response['data'][final]['value'] 
    except (KeyError, TypeError):
        print("Error fetching data")
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run(debug=True)
