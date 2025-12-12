import pandas as pd

def split_by_crypto(df: pd.DataFrame, crypto_list):
    subsets = {}
    for crypto in crypto_list:
        subsets[crypto] = df[df["cryptocurrency_name"] == crypto].copy()
    return subsets
