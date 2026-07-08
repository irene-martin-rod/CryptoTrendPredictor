import pandas as pd

def eliminate_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:

    '''
    Remove columns.

    Parameters:
        - df: a dataframe with values of cryptocurrencies
        - columns : list of columns names to remove

    Returns:
        - df
    '''
    return df.drop(columns=columns, errors="ignore")

def fill_dates(df: pd.DataFrame) -> pd.DataFrame:

    '''
    Fill missing dates and fill the columns "price_usd", "market_cap", "volume" with the last 
    known values

    Parameters:
        - df: a dataframe with values of cryptocurrencies

    Returns:
        - df
    '''
    df = df.copy()

    # Remove the hour
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    df = df.set_index("date").sort_index()

    full_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    df = df.reindex(full_range)

    df["date"] = df.index

    num_cols = ["price_usd", "market_cap", "volume"]

    df[num_cols] = df[num_cols].ffill()

    if "cryptocurrency_id" in df.columns:
        df["cryptocurrency_id"] = df["cryptocurrency_id"].ffill()

    return df.reset_index(drop=True)

