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

def get_bitcoin_market_cap():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    market_cap = soup.find('dd', class_='sc-f70bb44c-0 bCgkcs base-text').text
    market_cap = market_cap.split('$')[-1]  # Split by '$' and get the last part
    return '$' + market_cap  # Add '$' back to the beginning

def get_bitcoin_price_float():
    url = "https://coinmarketcap.com/currencies/bitcoin/"
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text').text
    # Remove dollar sign and commas, then convert to float
    price = price.replace('$', '').replace(',', '')
    return float(price)
