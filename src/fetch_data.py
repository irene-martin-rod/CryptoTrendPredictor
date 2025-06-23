import requests
from datetime import datetime
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from config import CRYPTOCURRENCIES  # Import list of cryptocurrencies from config.py

# Load environment variables from the .env file (adjust path if needed)
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_URL = os.getenv("POSTGRES_URL")

# API endpoint for CoinGecko
API_URL = "https://api.coingecko.com/api/v3/simple/price"

def save_to_db(data):
    '''
    Saves cryptocurrency data into the PostgreSQL database.

    Parameters:
    - data (dict): Cryptocurrency data with keys:
      date, crypto, price_usd, market_cap, volume_24h, change_24h
    '''

    if data is None:
        return
    
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        cursor = conn.cursor()

        # 1. Insert cryptocurrency if it doesn't exist and get its id
        cursor.execute(
            "INSERT INTO Cryptocurrencies (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
            (data['crypto'],)
        )
        conn.commit()

        cursor.execute(
            "SELECT id FROM Cryptocurrencies WHERE name = %s",
            (data['crypto'],)
        )
        crypto_id = cursor.fetchone()[0]

        # 2. Insert data into respective tables
        cursor.execute(
            "INSERT INTO Price (cryptocurrency_id, date, price_usd) VALUES (%s, %s, %s)",
            (crypto_id, data['date'], data['price_usd'])
        )
        cursor.execute(
            "INSERT INTO Market_capitalization (cryptocurrency_id, date, market_cap) VALUES (%s, %s, %s)",
            (crypto_id, data['date'], data['market_cap'])
        )
        cursor.execute(
            "INSERT INTO Transaction_volume_24h (cryptocurrency_id, date, volume) VALUES (%s, %s, %s)",
            (crypto_id, data['date'], data['volume_24h'])
        )
        cursor.execute(
            "INSERT INTO Value_change_24h (cryptocurrency_id, date, change) VALUES (%s, %s, %s)",
            (crypto_id, data['date'], data['change_24h'])
        )
        conn.commit()

    except Exception as e:
        print(f"Error saving data to DB: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_data_api(crypto):
    '''
    Fetches cryptocurrency data from the CoinGecko API.

    Parameters:
    - crypto (str): The cryptocurrency name.

    Returns:
    - dict: Dictionary containing cryptocurrency data with keys:
      date, crypto, price_usd, market_cap, volume_24h, change_24h
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
        response.raise_for_status()
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
    Fetches data for all cryptocurrencies listed in config.py and stores it in the DB.
    '''
    for crypto in CRYPTOCURRENCIES:
        print(f"Fetching data for {crypto}...")
        data = get_data_api(crypto)
        if data:
            save_to_db(data)
            print(f"Data for {crypto} saved successfully!")
        else:
            print(f"Failed to fetch data for {crypto}.")

if __name__ == "__main__":
    fetch_and_store_data()
