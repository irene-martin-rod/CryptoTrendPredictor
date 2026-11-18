# Pipeline for load data from a Supabase database

from src.supabase_client import supabase
import pandas as pd
from functools import reduce

def load_table(table_name: str) -> pd.DataFrame:
    '''
    Load all records from a specified Supabase table into a pandas DataFrame.

    Parameters:
        - table_name: name of the Supabase table to retrieve. The name is
          converted to lowercase before querying the database

    Returns:
        - df: pandas DataFrame containing all records retrieved from the
          specified table. Returns an empty DataFrame if no data is available
    '''
    table_name = table_name.lower()
    response = supabase.table(table_name).select("*").execute()
    data = response.data
    if data is None:
        return pd.DataFrame()
    return pd.DataFrame(data)


def load_all_data() -> pd.DataFrame:
    '''
    Load all main tables from Supabase and merge them into a unified DataFrame.

    Parameters:
        - None

    Returns:
        - unified_df: pandas DataFrame containing the combined cryptocurrency
          data from the Price, Market_capitalization, Transaction_volume_24h,
          Value_change_24h and Cryptocurrencies tables, with the following
          main columns:
            - cryptocurrency_id: unique identifier of the cryptocurrency
            - date: timestamp of the recorded data
            - price_usd: cryptocurrency price in USD
            - market_cap: cryptocurrency market capitalization
            - volume: 24-hour transaction volume
            - change: 24-hour percentage price change
            - cryptocurrency_name: name of the cryptocurrency
    '''
    # Load tables
    price = load_table("price")
    market = load_table("market_capitalization")
    volume = load_table("transaction_volume_24h")
    change = load_table("value_change_24h")
    crypto = load_table("cryptocurrencies")  # contains id, name

    # Columns to merge on
    common_cols = ["cryptocurrency_id", "date"]

    # Drop 'id' columns in data tables to avoid duplicates
    for df in [price, market, volume, change]:
        df.drop(columns=["id"], errors='ignore', inplace=True)

    # Merge all tables
    from functools import reduce
    dataframes = [price, market, volume, change]
    unified_df = reduce(lambda left, right: pd.merge(left, right, on=common_cols, how='outer'), dataframes)

    # Merge crypto name at the end
    unified_df = unified_df.merge(
        crypto[['id', 'name']],
        left_on="cryptocurrency_id",
        right_on="id",
        how="left"
    ).drop(columns=["id"]).rename(columns={"name": "cryptocurrency_name"})

    return unified_df
