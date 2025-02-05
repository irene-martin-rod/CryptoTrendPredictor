# **Obtain cryptocurrency data from the CoinGecko API**

import requests
from datetime import datetime
from database import save_to_db
from config import CRYPTOCURRENCIES  # Importamos la lista de criptos desde config.py



# API endpoint
API_URL = "https://api.coingecko.com/api/v3/simple/price"




def get_data_api(crypto):

    '''
    Fetches cryptocurrency data from the CoinGecko API.

    Parameters:
    - crypto (str): The name of the cryptocurrency to fetch.

    Returns:
    - dict: A dictionary containing the cryptocurrency data with the following keys:
        - date (str): The timestamp of the data.
        - crypto (str): The cryptocurrency name.
        - price_usd (float): The price of the cryptocurrency in USD.
        - market_cap (float): The market capitalization value.
        - volume_24h (float): The 24-hour transaction volume.
        - change_24h (float): The 24-hour percentage change.
      Returns None if an error occurs.
    '''
    

    params = {
        'ids': crypto, 
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raises an error if the request fails
        data = response.json()

        return {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crypto': crypto,
            'price_usd': data.get(crypto, {}).get('usd', 0),
            'market_cap': data.get(crypto, {}).get('usd_market_cap', 0),
            'volume_24h': data.get(crypto, {}).get('usd_24h_vol', 0),
            'change_24h': data.get(crypto, {}).get('usd_24h_change', 0)
        }
    except requests.RequestException as e:
        print(f"Error fetching data for {crypto}: {e}")
        return None





def fetch_and_store_data():
    '''
    Fetches cryptocurrency data for all cryptocurrencies listed in config.py
    and stores it in the database.
    '''

    for crypto in CRYPTOCURRENCIES:
        print(f"Fetching data for {crypto}...")
        data = get_data_api(crypto)
        if data:
            save_to_db(data)  # Guardamos todo de golpe con la función única
            print(f"Data for {crypto} saved successfully!")
        else:
            print(f"Failed to fetch data for {crypto}.")


if __name__ == "__main__":
    fetch_and_store_data()