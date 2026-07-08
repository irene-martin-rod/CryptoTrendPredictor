import pandas as pd

def export_csv(df: pd.Dataframe, path: str, include_index: bool = False) -> None:
    
    '''
    Exports dataframes.

    Parameters:
    - df: a dataframe with values of cryptocurrencies
    - path : directory which recesives the csv file
    - include_index: by default, it is False

    Returns:
        - None
    '''
    df.to_csv(path, index=include_index)
