import yaml
import pandas as pd
import numpy as np

from .split_crypto import split_by_crypto
from .clean import eliminate_columns, fill_dates
from .clean_prices import clean_crypto_timeseries
from .export import export_csv

def run_preprocess(df: pd.DataFrame,
                  config_path: str = "config/preprocess.yaml") -> None:
    '''
    Execute the complete preprocessing pipeline for cryptocurrency time series data.

    Parameters:
        - df: pandas DataFrame containing raw data for multiple cryptocurrencies
        - config_path: path to the YAML configuration file specifying the
          output folder and preprocessing options (default="config/preprocess.yaml")

    Returns:
        - None: splits the dataset by cryptocurrency, cleans each time series,
          optionally fills missing calendar dates, removes unnecessary columns
          and exports one cleaned CSV file per cryptocurrency to the configured
          output folder
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
