import requests
from bs4 import BeautifulSoup
import time

def get_bitcoin_price():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find('div', class_='priceValue').text
    return price

while True:
    print("Current Bitcoin price:", get_bitcoin_price())
    time.sleep(10)  # Wait for 10 seconds before refreshing the price