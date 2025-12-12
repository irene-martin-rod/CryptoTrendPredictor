import yaml
import pandas as pd
import numpy as np
from .clean import eliminate_columns, fill_dates
from .split_crypto import split_by_crypto
from .export import export_csv

def run_preprocess(config_path="config/preprocess.yaml"):
    # Load config
    config = yaml.safe_load(open(config_path))

    df = pd.read_csv(config["input_path"])
    df["date"] = pd.to_datetime(df["date"]).dt.date

    df = eliminate_columns(df, config["columns_to_drop"])

    # Split
    subsets = split_by_crypto(df, config["cryptocurrencies"])

    # Process each crypto
    for name, subdf in subsets.items():
        if config["fill_missing_dates"]:
            subdf = fill_dates(subdf)

        subdf = eliminate_columns(subdf, ["cryptocurrency_name"])

        output_path = f'{config["output_folder"]}/{name}.csv'
        export_csv(subdf, output_path, include_index=config["include_index"])

    print("Preprocess completed")
