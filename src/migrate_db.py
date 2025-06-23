import os
import sqlite3
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the root folder
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise ValueError("POSTGRES_URL is not defined in the .env file")

print("POSTGRES_URL loaded successfully")

# Connect to SQLite (adjust path if needed)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "data", "raw", "crypto_data.db")
sqlite_conn = sqlite3.connect(db_path)
sqlite_cursor = sqlite_conn.cursor()

# Connect to PostgreSQL
pg_conn = psycopg2.connect(POSTGRES_URL)
pg_cursor = pg_conn.cursor()

# Create tables in PostgreSQL
print("Creating tables in PostgreSQL...")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS Cryptocurrencies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS Price (
    id SERIAL PRIMARY KEY,
    cryptocurrency_id INTEGER REFERENCES Cryptocurrencies(id),
    date TIMESTAMP NOT NULL,
    price_usd REAL
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS Market_capitalization (
    id SERIAL PRIMARY KEY,
    cryptocurrency_id INTEGER REFERENCES Cryptocurrencies(id),
    date TIMESTAMP NOT NULL,
    market_cap REAL
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS Transaction_volume_24h (
    id SERIAL PRIMARY KEY,
    cryptocurrency_id INTEGER REFERENCES Cryptocurrencies(id),
    date TIMESTAMP NOT NULL,
    volume REAL
);
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS Value_change_24h (
    id SERIAL PRIMARY KEY,
    cryptocurrency_id INTEGER REFERENCES Cryptocurrencies(id),
    date TIMESTAMP NOT NULL,
    change REAL
);
""")

pg_conn.commit()
print("Tables created or verified successfully.")

# Insert Cryptocurrencies from SQLite into PostgreSQL
sqlite_cursor.execute("SELECT id, name FROM Cryptocurrencies")
cryptos = sqlite_cursor.fetchall()
for cid, name in cryptos:
    pg_cursor.execute(
        "INSERT INTO Cryptocurrencies (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (name,)
    )
pg_conn.commit()

# Create a name to id map for PostgreSQL cryptocurrencies
pg_cursor.execute("SELECT id, name FROM Cryptocurrencies")
pg_cryptos = {name: cid for cid, name in pg_cursor.fetchall()}

def migrate_table(sqlite_table, pg_table, columns):
    sqlite_cursor.execute(f"SELECT cryptocurrency_id, date, {', '.join(columns)} FROM {sqlite_table}")
    rows = sqlite_cursor.fetchall()

    for row in rows:
        sqlite_crypto_id = row[0]
        date = row[1]
        values = row[2:]

        # Get crypto name in SQLite
        sqlite_cursor.execute("SELECT name FROM Cryptocurrencies WHERE id = ?", (sqlite_crypto_id,))
        name = sqlite_cursor.fetchone()[0]

        # Get crypto id in PostgreSQL
        pg_crypto_id = pg_cryptos.get(name)
        if pg_crypto_id is None:
            continue

        placeholders = ", ".join(["%s"] * (2 + len(columns)))
        pg_cursor.execute(
            f"INSERT INTO {pg_table} (cryptocurrency_id, date, {', '.join(columns)}) VALUES ({placeholders})",
            (pg_crypto_id, date, *values)
        )

print("Migrating Price table...")
migrate_table("Price", "Price", ["price_usd"])

print("Migrating Market_capitalization table...")
migrate_table("Market_capitalization", "Market_capitalization", ["market_cap"])

print("Migrating Transaction_volume_24h table...")
migrate_table("Transaction_volume_24h", "Transaction_volume_24h", ["volume"])

print("Migrating Value_change_24h table...")
migrate_table("Value_change_24h", "Value_change_24h", ["change"])

pg_conn.commit()

sqlite_conn.close()
pg_conn.close()

print("✅ Migration completed successfully.")
