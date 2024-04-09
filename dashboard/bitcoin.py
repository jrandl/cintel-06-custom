import requests
from bs4 import BeautifulSoup

def get_bitcoin_price():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text').text
    return price

#print("Current Bitcoin price:", get_bitcoin_price())
