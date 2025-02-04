# **DATABASE SQL**

import sqlite3
from config import DB_NAME  # Import database name from config.py



def init_db():
    """Creates and initializes the database with necessary tables."""
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
    """
    Inserts a cryptocurrency into the database (if it doesn't exist) and retrieves its ID.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO Cryptocurrencies (name) VALUES (?)", (crypto,))
    conn.commit()
    
    cursor.execute("SELECT id FROM Cryptocurrencies WHERE name = ?", (crypto,))
    crypto_id = cursor.fetchone()[0]
    
    conn.close()
    return crypto_id




if __name__ == "__main__":
    init_db()  # Run this script to initialize the database
    print("Database initialized successfully!")