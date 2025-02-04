# **Obtain cryptocurrency data from the CoinGecko API**

import requests
from datetime import datetime
from database import save_price, save_market_cap, save_volume, save_change
from config import CRYPTOCURRENCIES  # Importamos la lista de criptos desde config.py



# API endpoint
API_URL = "https://api.coingecko.com/api/v3/simple/price"




# Function to get data from the API
def get_data_api(crypto):
    params = {
        'ids': crypto, 
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    
    response = requests.get(API_URL, params=params)
    
    try:
        data = response.json()
        return {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crypto': crypto,
            'price_usd': data[crypto]['usd'],
            'volume_24h': data[crypto]['usd_24h_vol'],
            'market_cap': data[crypto]['usd_market_cap'],
            'change_24h': data[crypto]['usd_24h_change']
        }
    except KeyError:
        return None
    




# Function to fetch and store data in the database
def fetch_and_store_data():
    for crypto in CRYPTOCURRENCIES:  # Ahora usa la lista de config.py
        data = get_data_api(crypto)
        if data:
            save_price(data['crypto'], data['date'], data['price_usd'])
            save_market_cap(data['crypto'], data['date'], data['market_cap'])
            save_volume(data['crypto'], data['date'], data['volume_24h'])
            save_change(data['crypto'], data['date'], data['change_24h'])
    print("Data successfully fetched and stored!")




if __name__ == "__main__":
    fetch_and_store_data()