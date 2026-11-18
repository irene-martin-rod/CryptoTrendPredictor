import pandas as pd

def eliminate_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    '''
    Remove the specified columns from a cryptocurrency DataFrame.

    Parameters:
        - df: pandas DataFrame containing cryptocurrency data
        - columns: list of column names to remove from the DataFrame

    Returns:
        - df: DataFrame with the specified columns removed; columns that
          do not exist in the DataFrame are ignored
    '''
    return df.drop(columns=columns, errors="ignore")



def fill_dates(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Fill missing dates and forward-fill numerical variables using the last known values.

    Parameters:
        - df: pandas DataFrame containing cryptocurrency time series data,
          including the columns 'date', 'price_usd', 'market_cap' and 'volume'

    Returns:
        - df: DataFrame with a complete daily date range between the minimum
          and maximum dates, where missing values in 'price_usd', 'market_cap'
          and 'volume' are filled using the last available observations.
          If present, 'cryptocurrency_id' is also forward-filled
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

