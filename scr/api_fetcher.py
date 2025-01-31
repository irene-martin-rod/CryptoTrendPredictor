# **Obtain cryptocurrency data from the CoinGecko API**

### Import libraries
import requests
import sqlite3
from datetime import datetime

# List of cryptocurrencies
cryptocurrencies = [
    "bitcoin", "ethereum", "tether", "binancecoin", "usd-coin", 
    "ripple", "cardano", "dogecoin", "solana", "matic-network"
]

# Create and connect to a SQL database
def init_db():
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    
    # Create main cryptocurrency table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cryptocurrencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create price table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptocurrency_id INTEGER,
            date DATETIME NOT NULL,
            price_usd REAL,
            price_eur REAL,
            FOREIGN KEY (cryptocurrency_id) REFERENCES Cryptocurrencies(id)
        )
    ''')
    
    # Create market capitalization table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Market_capitalization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptocurrency_id INTEGER,
            date DATETIME NOT NULL,
            market_cap REAL,
            FOREIGN KEY (cryptocurrency_id) REFERENCES Cryptocurrencies(id)
        )
    ''')
    
    # Create transaction volume table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transaction_volume_24h (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptocurrency_id INTEGER,
            date DATETIME NOT NULL,
            volume REAL,
            FOREIGN KEY (cryptocurrency_id) REFERENCES Cryptocurrencies(id)
        )
    ''')
    
    # Create value change table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Value_change_24h (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptocurrency_id INTEGER,
            date DATETIME NOT NULL,
            change REAL,
            FOREIGN KEY (cryptocurrency_id) REFERENCES Cryptocurrencies(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Get cryptocurrency ID from database
def get_crypto_id(crypto):
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO Cryptocurrencies (name) VALUES (?)", (crypto,))
    conn.commit()
    
    cursor.execute("SELECT id FROM Cryptocurrencies WHERE name = ?", (crypto,))
    crypto_id = cursor.fetchone()[0]
    conn.close()
    return crypto_id

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
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'crypto': crypto,
            'price_usd': data[crypto]['usd'],
            'price_eur': data[crypto]['eur'],
            'volume_24h': data[crypto]['usd_24h_vol'],
            'market_cap': data[crypto]['usd_market_cap'],
            'change_24h': data[crypto]['usd_24h_change']
        }
    except KeyError:
        return None

# Save data in SQL database
def save_to_db(data):
    if data is None:
        return
    
    conn = sqlite3.connect("crypto_data.db")
    cursor = conn.cursor()
    
    crypto_id = get_crypto_id(data['crypto'])
    
    cursor.execute('''
        INSERT INTO Price (cryptocurrency_id, date, price_usd, price_eur)
        VALUES (?, ?, ?, ?)
    ''', (crypto_id, data['date'], data['price_usd'], data['price_eur']))
    
    cursor.execute('''
        INSERT INTO Market_capitalization (cryptocurrency_id, date, market_cap)
        VALUES (?, ?, ?)
    ''', (crypto_id, data['date'], data['market_cap']))
    
    cursor.execute('''
        INSERT INTO Transaction_volume_24h (cryptocurrency_id, date, volume)
        VALUES (?, ?, ?)
    ''', (crypto_id, data['date'], data['volume_24h']))
    
    cursor.execute('''
        INSERT INTO Value_change_24h (cryptocurrency_id, date, change)
        VALUES (?, ?, ?)
    ''', (crypto_id, data['date'], data['change_24h']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Obtaining data and saving in SQL database
    for crypto in cryptocurrencies:
        data_api = get_data_api(crypto)
        save_to_db(data_api)