# **DATABASE SQL**

import sqlite3
from config import DB_NAME  # Import database name from config.py



def init_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    '''
    Initialize the SQLite database and create the required tables if they do not exist.

    Tables:
        - Cryptocurrencies: stores unique cryptocurrency names
        - Price: stores historical price data in USD
        - Market_capitalization: stores historical market capitalization data
        - Transaction_volume_24h: stores historical 24-hour transaction volume data
        - Value_change_24h: stores historical 24-hour price change data

    Parameters:
        - None

    Returns:
        - conn: SQLite database connection object
        - cursor: SQLite cursor object used to execute database queries
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
    return conn, cursor
    #conn.close()




def get_crypto_id(crypto: str) -> int:
    '''
    Retrieve the ID of a cryptocurrency from the database, inserting it if it does not exist.

    Parameters:
        - crypto: name of the cryptocurrency to retrieve or insert

    Returns:
        - crypto_id: integer identifier of the cryptocurrency in the database
    '''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO Cryptocurrencies (name) VALUES (?)", (crypto,))
    conn.commit()
    
    cursor.execute("SELECT id FROM Cryptocurrencies WHERE name = ?", (crypto,))
    crypto_id = cursor.fetchone()[0]
    
    conn.close()
    return crypto_id



def save_to_db(data: dict | None) -> None:
    '''
    Save cryptocurrency market data into the SQLite database.

    Parameters:
        - data: dictionary containing the cryptocurrency information with
          the following keys:
            - date: timestamp of the recorded data
            - crypto: name of the cryptocurrency
            - price_usd: cryptocurrency price in USD
            - market_cap: cryptocurrency market capitalization
            - volume_24h: 24-hour transaction volume
            - change_24h: 24-hour percentage price change

    Returns:
        - None: inserts the cryptocurrency data into the corresponding
          database tables. If data is None, no operation is performed
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