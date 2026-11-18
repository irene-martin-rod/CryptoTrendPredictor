import pandas as pd

def split_by_crypto(df: pd.DataFrame, crypto_col: str) -> dict[str, pd.DataFrame]:
    '''
    Split a DataFrame into separate DataFrames, one for each cryptocurrency.

    Parameters:
        - df: pandas DataFrame containing data for multiple cryptocurrencies
        - crypto_col: name of the column identifying each cryptocurrency

    Returns:
        - subsets: dictionary where cryptocurrency names are used as keys
          and their corresponding DataFrames are stored as values
    '''
    subsets = {}
    for crypto in df[crypto_col].unique():
        subsets[crypto] = df[df[crypto_col] == crypto].copy()
    return subsets
