import pandas as pd


def fill_missing_prices(df: pd.DataFrame) -> pd.DataFrame:

    '''
    Fill NA in price_usd if there is a price_use and change values the next day

    Parameters:
    df (pd.DataFrame): A DataFrame

    Returns:
    pd.DataFrame: A dataframe without the colums
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
    Impute NAs using values of previous days.

    Parameters:
    df (pd.DataFrame): A DataFrame

    Returns:
    pd.DataFrame: A dataframe without the columns
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
    Full cleaning pipeline for a single cryptocurrency.

    Parameters:
        - df: raw Pandas dataframe
    
    Returns:
        df: clean Pandas dataframe
    '''
    
    df = fill_missing_prices(df)
    df = fill_rest_variables(df)
    return df