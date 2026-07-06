import yaml
import pandas as pd
import numpy as np

from .split_crypto import split_by_crypto
from .clean import eliminate_columns, fill_dates
from .clean_prices import clean_crypto_timeseries
from .export import export_csv

def run_preprocess(df: pd.DataFrame, config_path: str = "config/preprocess.yaml"):

    '''
    End-to-end preprocessing pipeline for cryptocurrency time series data.

    This function:
    1. Splits the data by cryptocurrency.
    2. Cleans each cryptocurrency time series:
       - Imputes missing prices using next-day price and percentage change.
       - Forward-fills non-target variables.
       - Removes invalid or incomplete target values.
    3. Optionally fills missing calendar dates.
    4. Exports one cleaned CSV file per cryptocurrency.

    Parameters:
        - df: a dataframe with values of cryptocurrencies
        - config_path : str. Path to the YAML configuration file controlling input/output paths
        and preprocessing options.

    Returns:
        - None. This function does not return any object. Cleaned datasets are written to disk as CSV files
    '''

    # Load configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Ensure date format
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Split by cryptocurrency
    subsets = split_by_crypto(
        df,
        crypto_col="cryptocurrency_name"
    )

    for name, subdf in subsets.items():

        # Clean missing values
        subdf = clean_crypto_timeseries(subdf)

        # Fill missing dates
        if config["fill_missing_dates"]:
            subdf = fill_dates(subdf)

        # Remove unnecessary columns
        subdf = eliminate_columns(
            subdf,
            ["cryptocurrency_name"]
        )

        # Export
        export_csv(
            subdf,
            f"{config['output_folder']}/{name}.csv",
            include_index=False
        )

    print("Preprocessing completed.")
