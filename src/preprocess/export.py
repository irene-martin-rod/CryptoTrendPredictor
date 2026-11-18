import pandas as pd

def export_csv(df: pd.DataFrame, path: str, include_index: bool = False) -> None:
    '''
    Export a cryptocurrency DataFrame to a CSV file.

    Parameters:
        - df: pandas DataFrame containing cryptocurrency data
        - path: file path where the CSV file will be saved
        - include_index: whether to include the DataFrame index in the
          exported CSV file (default=False)

    Returns:
        - None: saves the DataFrame as a CSV file at the specified path
    '''
    df.to_csv(path, index=include_index)
