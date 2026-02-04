import pandas as pd

def split_by_crypto(df: pd.DataFrame, crypto_col: str) -> dict:

    '''
    Split a dataframe into multiple dataframes, one per cryptocurrency.

    Parameters:
        - df : pd.DataFrame. Input dataframe.
        - crypto_col : str. Column name identifying the cryptocurrency.

    Returns:
        - dict[str, pd.DataFrame]. Dictionary with cryptocurrency names as keys and dataframes as values
    '''

    subsets = {}
    for crypto in df[crypto_col].unique():
        subsets[crypto] = df[df[crypto_col] == crypto].copy()
    return subsets
