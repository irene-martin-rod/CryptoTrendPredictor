# Migrate a SQLite to PostgreSQL for upload database to Supabase

import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")

# Conections
# Root path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "data", "raw", "crypto_data.db")

sqlite_conn = sqlite3.connect(db_path)
sqlite_cursor = sqlite_conn.cursor()

POSTGRES_URL = os.getenv("POSTGRES_URL")
pg_conn = psycopg2.connect(POSTGRES_URL)
pg_cursor = pg_conn.cursor()

# Migrate
sqlite_cursor.execute("SELECT id, name FROM Cryptocurrencies")
cryptos = sqlite_cursor.fetchall()
for cid, name in cryptos:
    pg_cursor.execute(
        "INSERT INTO Cryptocurrencies (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (name,)
    )

# Create a map
pg_cursor.execute("SELECT id, name FROM Cryptocurrencies")
pg_cryptos = {name: cid for cid, name in pg_cursor.fetchall()}

def migrate_table(sqlite_table, pg_table, columns):
    sqlite_cursor.execute(f"SELECT cryptocurrency_id, date, {', '.join(columns)} FROM {sqlite_table}")
    rows = sqlite_cursor.fetchall()
    
    for row in rows:
        sqlite_crypto_id = row[0]
        date = row[1]
        values = row[2:]
        
        sqlite_cursor.execute("SELECT name FROM Cryptocurrencies WHERE id = ?", (sqlite_crypto_id,))
        name = sqlite_cursor.fetchone()[0]
        
        pg_crypto_id = pg_cryptos.get(name)
        if pg_crypto_id is None:
            continue
        
        placeholders = ", ".join(["%s"] * (2 + len(columns)))
        pg_cursor.execute(
            f"INSERT INTO {pg_table} (cryptocurrency_id, date, {', '.join(columns)}) VALUES ({placeholders})",
            (pg_crypto_id, date, *values)
        )

migrate_table("Price", "Price", ["price_usd"])
migrate_table("Market_capitalization", "Market_capitalization", ["market_cap"])
migrate_table("Transaction_volume_24h", "Transaction_volume_24h", ["volume"])
migrate_table("Value_change_24h", "Value_change_24h", ["change"])

pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("✅ Completed migration to Supabase")