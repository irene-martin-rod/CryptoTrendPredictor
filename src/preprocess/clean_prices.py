import pandas as pd


def fill_missing_prices(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Fill missing price values using the next day's price and percentage change.

    Parameters:
        - df: pandas DataFrame containing the time series data, including
          the columns 'date', 'price_usd' and 'change'

    Returns:
        - df: DataFrame with missing values in 'price_usd' filled when
          the next day's price and percentage change are available
    '''

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    for i in range(len(df) - 1):
        if pd.isna(df.loc[i, 'price_usd']):
            next_price = df.loc[i + 1, 'price_usd']
            next_change = df.loc[i + 1, 'change']

            if not pd.isna(next_price) and not pd.isna(next_change):
                df.loc[i, 'price_usd'] = next_price / (1 + next_change / 100)

    return df


def fill_rest_variables(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Impute missing values in the remaining variables using previous observations.

    Parameters:
        - df: pandas DataFrame containing the time series data, including
          the columns 'date', 'price_usd', 'change' and 'cryptocurrency_name'

    Returns:
        - df: DataFrame with missing values in the remaining variables
          forward-filled, the 'change' column removed and rows without
          a valid 'price_usd' value dropped
    '''

    df = df.sort_values('date').reset_index(drop=True)

    features_to_fill = df.columns.difference(
        ['date', 'price_usd', 'change', 'cryptocurrency_name']
    )

    df[features_to_fill] = df[features_to_fill].ffill()

    df = df.drop(columns=['change'])
    df = df.dropna(subset=['price_usd']).reset_index(drop=True)

    return df


def clean_crypto_timeseries(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Apply the complete cleaning pipeline to a single cryptocurrency time series.

    Parameters:
        - df: raw pandas DataFrame containing the cryptocurrency time series
          data, including missing values

    Returns:
        - df: cleaned pandas DataFrame with missing prices imputed,
          remaining variables forward-filled and invalid price rows removed
    '''
    
    df = fill_missing_prices(df)
    df = fill_rest_variables(df)
    return df