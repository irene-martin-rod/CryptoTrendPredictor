# **CREATE DATABASE, GET DATA AND SAVE IN DB**


from database import init_db
from fetch_data import fetch_and_store_data

if __name__ == "__main__":
    init_db()  # Initialize database
    fetch_and_store_data()  # Fetch and save data
    print("Data successfully fetched and stored!")