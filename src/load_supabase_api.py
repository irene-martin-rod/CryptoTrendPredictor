# Pipeline for load data from a Supabase database

from supabase_client import supabase
import pandas as pd
from functools import reduce

def load_table(table_name: str) -> pd.DataFrame:
    '''
    Load all records from a Supabase table into a DataFrame.
    Convert the name to lowercase to avoid case-sensitive errors.

    Parameters:
        - table-name: name of a spacific table of a Supabase database
    
    Returns:
        - data: a pd.Dataframe with the records.
    '''
    table_name = table_name.lower()
    response = supabase.table(table_name).select("*").execute()
    data = response.data
    if data is None:
        return pd.DataFrame()
    return pd.DataFrame(data)




def load_all_data() -> pd.DataFrame:
    '''
    Load all main tables and combines in a unified dtaframe

    Returns:
        - unified_df: a pd.DataFrame
    '''
    # Load tables
    price = load_table("price")
    market = load_table("market_capitalization")
    volume = load_table("transaction_volume_24h")
    change = load_table("value_change_24h")
    crypto = load_table("cryptocurrencies")

    # Add the name of the cryptocurrency in each table
    for df in [price, market, volume, change]:
        df.merge(crypto[['id', 'name']], left_on="cryptocurrency_id", right_on="id", 
                 suffixes=("", "_crypto"))

    # Merge all Dataframe
    dataframes = [price, market, volume, change]
    common_cols = ["id", "cryptocurrency_id", "date"]
    unified_df = reduce(lambda left, right: pd.merge(left, right, on=common_cols, how='outer'), 
                        dataframes)

    # Add cryptocurrency name column from criptocurrency_id
    unified_df = unified_df.merge(crypto[['id', 'name']], left_on="cryptocurrency_id", 
                                  right_on="id", suffixes=("", "_crypto"))

    return unified_df
