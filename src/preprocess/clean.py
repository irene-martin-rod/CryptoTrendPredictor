import pandas as pd

def eliminate_columns(df: pd.DataFrame, columns):
    return df.drop(columns=columns, errors="ignore")

def fill_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

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

