import requests

def get_latest_btc_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    api_key = '802cc676-5f93-4cab-ae31-fa7ddd98ef01'  # Replace with your API key
    headers = {
        "X-CMC_PRO_API_KEY": api_key,
        "Accept": "application/json"
    }
    parameters = {
        "symbol": "BTC"
    }

    response = requests.get(url, headers=headers, params=parameters)
    json_data = response.json()
    btc_price = json_data['data']['BTC']['quote']['USD']['price']

    return btc_price

print("Current Bitcoin price: $", get_latest_btc_price())
