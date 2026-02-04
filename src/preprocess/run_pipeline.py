import yaml
import pandas as pd
import numpy as np

from .split_crypto import split_by_crypto
from .clean import eliminate_columns, fill_dates
from .clean_prices import clean_crypto_timeseries
from .export import export_csv

def run_preprocess(config_path: str = "config/preprocess.yaml"):

    '''
    End-to-end preprocessing pipeline for cryptocurrency time series data.

    This function:
    1. Loads a raw dataset from a CSV file.
    2. Splits the data by cryptocurrency.
    3. Cleans each cryptocurrency time series:
       - Imputes missing prices using next-day price and percentage change.
       - Forward-fills non-target variables.
       - Removes invalid or incomplete target values.
    4. Optionally fills missing calendar dates.
    5. Exports one cleaned CSV file per cryptocurrency.

    Parameters:
        - config_path : str. Path to the YAML configuration file controlling input/output paths
        and preprocessing options.

    Returns:
        - None. This function does not return any object. Cleaned datasets are written to disk as CSV files
    '''

    # Load config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Load data
    df = pd.read_csv(config["input_path"])
    df["date"] = pd.to_datetime(df["date"])

    # Split by crypto FIRST (logical separation)
    subsets = split_by_crypto(df, crypto_col="cryptocurrency_name")

    for name, subdf in subsets.items():

        # Clean price data (your Binance logic, generalized)
        subdf = clean_crypto_timeseries(subdf)

        # Fill missing dates
        if config["fill_missing_dates"]:
            subdf = fill_dates(subdf)

        # Drop crypto name (no leakage)
        subdf = eliminate_columns(subdf, ["cryptocurrency_name"])

        # Export
        output_path = f'{config["output_folder"]}/{name}.csv'
        export_csv(subdf, output_path, include_index=False)

    print("Preprocess completed")
