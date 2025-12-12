import pandas as pd

def eliminate_columns(df: pd.DataFrame, columns):
    return df.drop(columns=columns, errors="ignore")

def fill_dates(df: pd.DataFrame):
    df = df.set_index("date")
    full_range = pd.date_range(df.index.min(), df.index.max(), freq="D")
    df = df.reindex(full_range)
    df.index.name = "date"
    return df
