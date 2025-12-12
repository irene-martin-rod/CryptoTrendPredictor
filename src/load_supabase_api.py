# Pipeline for load data from a Supabase database

from supabase_client import supabase
import pandas as pd
from functools import reduce

def load_table(table_name: str) -> pd.DataFrame:
    table_name = table_name.lower()
    response = supabase.table(table_name).select("*").execute()
    data = response.data
    if data is None:
        return pd.DataFrame()
    return pd.DataFrame(data)


def load_all_data() -> pd.DataFrame:
    """
    Load all main tables from Supabase and combine them into a unified dataframe.
    Returns a dataframe with a standard column 'cryptocurrency_name'.
    """
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
