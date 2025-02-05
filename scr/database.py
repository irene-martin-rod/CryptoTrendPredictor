# **DATABASE SQL**

import sqlite3
from config import DB_NAME  # Import database name from config.py



def init_db():

    '''
    Initializes the SQLite database and creates the necessary tables if they do not exist.
    
    Tables:
    - Cryptocurrencies: Stores unique cryptocurrency names.
    - Price: Stores historical price data in USD.
    - Market_capitalization: Stores historical market capitalization data.
    - Transaction_volume_24h: Stores 24-hour transaction volume data.
    - Value_change_24h: Stores 24-hour price change data.
    '''
    
    conn = sqlite3.connect(DB_NAME)
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




def get_crypto_id(crypto):

    '''
    Retrieves the cryptocurrency ID from the database. 
    If the cryptocurrency does not exist, it is inserted into the database.

    Parameters:
    - crypto (str): The name of the cryptocurrency.

    Returns:
    - int: The ID of the cryptocurrency in the database.
    '''
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO Cryptocurrencies (name) VALUES (?)", (crypto,))
    conn.commit()
    
    cursor.execute("SELECT id FROM Cryptocurrencies WHERE name = ?", (crypto,))
    crypto_id = cursor.fetchone()[0]
    
    conn.close()
    return crypto_id



def save_to_db(data):
    '''
    Saves cryptocurrency data into the database.

    Parameters:
    - data (dict): Dictionary containing cryptocurrency data with the following keys:
        - date (str): The timestamp of the data.
        - crypto (str): The cryptocurrency name.
        - price_usd (float): The price of the cryptocurrency in USD.
        - market_cap (float): The market capitalization value.
        - volume_24h (float): The 24-hour transaction volume.
        - change_24h (float): The 24-hour percentage change.
        
    '''
    
    if data is None:
        return
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    crypto_id = get_crypto_id(data['crypto'])
    
    cursor.execute('''
        INSERT INTO Price (cryptocurrency_id, date, price_usd)
        VALUES (?, ?, ?)
    ''', (crypto_id, data['date'], data['price_usd']))

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
    init_db()  # Run this script to initialize the database
    print("Database initialized successfully!")