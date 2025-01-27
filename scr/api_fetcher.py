# **Obtain data of cryptocurrencies from the CoinGecko API 

### Import libraries

import requests
import sqlite3
from datetime import datetime

# Lista de criptomonedas
cryptocurrencies = [
    "bitcoin", "ethereum", "tether", "binancecoin", "usd-coin", 
    "ripple", "cardano", "dogecoin", "solana", "matic-network"
]

# Create and connet to a SQL database
def init_db():
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            crypto TEXT NOT NULL,
            price_usd REAL,
            price_eur REAL,
            volume_24h REAL,
            market_cap REAL,
            change_24h REAL
        )
    ''')
    conn.commit()
    conn.close()

# Obtain data from API
def get_data_api(crypto):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': crypto, 
        'vs_currencies': 'usd,eur',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    response = requests.get(url, params=params)

    try:
        data = response.json()
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'crypto': crypto,
            'price_usd': data[crypto]['usd'],
            'price_eur': data[crypto]['eur'],
            'volume_24h': data[crypto]['usd_24h_vol'],
            'market_cap': data[crypto]['usd_market_cap'],
            'change_24h': data[crypto]['usd_24h_change']
        }
    except KeyError:
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'crypto': crypto,
            'price_usd': None,
            'price_eur': None,
            'volume_24h': None,
            'market_cap': None,
            'change_24h': None
        }

# Save data in SQL databse
def save_to_db(data):
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO crypto_data (date, crypto, price_usd, price_eur, volume_24h, market_cap, change_24h)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['date'], data['crypto'], data['price_usd'], data['price_eur'], 
          data['volume_24h'], data['market_cap'], data['change_24h']))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Init databse
    init_db()

    # Obtaining data and saving in SQL database
    for crypto in cryptocurrencies:
        data_api = get_data_api(crypto)
        save_to_db(data_api)