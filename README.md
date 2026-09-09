# CryptoTrendPredictor

Predicting cryptocurrency price and trend dynamics using time-series analysis and machine learning.

## Project structure

```text
/CryptoTrendPredictor/

├── .github/
│   └── workflows/
│       └── run_main.yml              # GitHub Actions workflow for automated data updates
│
├── config/
│   └── preprocess.yaml               # Preprocessing configuration
│
├── data/
│   ├── processed/
│   │   ├── binancecoin.csv
│   │   ├── bitcoin.csv
│   │   ├── ethereum.csv
│   │   ├── ripple.csv
│   │   ├── tether.csv
│   │   └── usd-coin.csv
│   │
│   └── raw/
│       ├── crypto_data.db             # Local SQLite database
│       └── db_04022026.csv           # Raw dataset
│
├── notebooks/
│   ├── 1-obtain_data.ipynb            # Data acquisition and preprocessing
│   └── 2-eda_crypto_*.ipynb           # Exploratory Data Analysis for each cryptocurrency
│
├── src/
│   ├── analysis/
│   │   └── eda.py                    # EDA and time-series analysis functions
│   │
│   └── preprocess/
│       ├── __init__.py
│       ├── clean_prices.py            # Price cleaning and missing-price handling
│       ├── clean.py                   # Data cleaning and missing-date handling
│       ├── export.py                  # CSV export utilities
│       ├── run_pipeline.py            # Preprocessing pipeline
│       └── split_crypto.py            # Split data by cryptocurrency
│
│   ├── config.py                      # Configuration parameters
│   ├── database.py                    # Database initialization and storage
│   ├── fetch_data.py                  # Cryptocurrency data acquisition
│   ├── load_supabase_api.py           # Data loading from Supabase
│   ├── main.py                        # Main automated pipeline
│   ├── migrate_db.py                  # SQLite → PostgreSQL migration
│   └── supabase_client.py             # Supabase/PostgreSQL connection
```

## Overview

**CryptoTrendPredictor** is a modular project for analyzing cryptocurrency time series and developing models to predict future price behavior and market trends.

The project is currently focused on six cryptocurrencies:

- Bitcoin
- Ethereum
- Binance Coin
- Ripple
- Tether
- USD Coin

The project is divided into several stages:

```text
Data Acquisition
       ↓
Preprocessing
       ↓
Processed Time Series
       ↓
Exploratory Data Analysis
       ↓
Target Definition
       ↓
Feature Engineering
       ↓
Dataset Creation
       ↓
Modeling and Evaluation
```

At the current stage, **data acquisition, preprocessing, and exploratory data analysis have been completed**. Target definition and modeling are the next stages of development.

---

# Data Pipeline

## Raw Data

Historical cryptocurrency data is collected through the project's data acquisition pipeline.

The dataset contains variables such as:

- `date`
- `price_usd`
- `market_cap`
- `volume`
- `change`
- `cryptocurrency_name`

The data is stored in a PostgreSQL database hosted through Supabase and can be exported into individual processed CSV files for each cryptocurrency.

---

## Preprocessing

The preprocessing pipeline performs several operations before the data is used for analysis.

### Cryptocurrency separation

The raw dataset is divided into individual time series, one for each cryptocurrency.

The current processed datasets are:

```text
bitcoin.csv
ethereum.csv
binancecoin.csv
ripple.csv
tether.csv
usd-coin.csv
```

### Price cleaning

Missing prices are reconstructed when possible using the following observation and its percentage change.

### Missing dates

The time series are converted to a daily frequency. Missing calendar dates are inserted and the corresponding variables are filled according to the preprocessing strategy.

During development, timestamp normalization was required because the original observations contained different times of day. Dates are therefore normalized before the daily time series is completed.

### Output

The resulting datasets are stored in:

```text
data/processed/
```

Each cryptocurrency is represented by an independent daily time series.

---

# Exploratory Data Analysis

The EDA stage has been performed independently for all six cryptocurrencies.

The analysis currently includes:

1. Price and market variables
2. Returns and volatility
3. Autocorrelation
4. Trend analysis
5. Slope distributions
6. Moving averages
7. Time-series decomposition

The EDA is intended to understand the characteristics of the data before defining prediction targets and machine-learning features.

---

## 1. Price and market variables

The evolution of:

- `price_usd`
- `market_cap`
- `volume`

is analyzed over time.

The analysis shows two broad behavioral groups:

### Volatile cryptocurrencies

- Bitcoin
- Ethereum
- Binance Coin
- Ripple

These assets show considerably larger price movements and more variability.

### Stablecoins

- Tether
- USD Coin

Their prices remain very close to USD 1, resulting in substantially smaller price movements and slope values.

This distinction is important for the subsequent modeling stage because the same absolute variation does not have the same meaning across all cryptocurrencies.

---

## 2. Returns and volatility

Percentage returns are calculated from the cryptocurrency price:

```python
returns = price_usd.pct_change() * 100
```

Rolling volatility is then calculated using a 7-day window.

This analysis provides information about the short-term variability of each cryptocurrency and will later be useful when constructing predictive features.

---

## 3. Autocorrelation

Autocorrelation is analyzed for both:

- cryptocurrency prices
- percentage returns

using up to 30 lags.

This provides information about the temporal dependence present in the series and helps motivate the use of time-series and lag-based approaches in later stages.

---

## 4. Trend analysis

Rolling linear-regression slopes are calculated using three windows:

```text
7 days
14 days
30 days
```

The slope is calculated on the logarithm of the price, allowing the trend measure to represent relative rather than absolute price changes.

The three windows capture different types of behavior:

```text
7-day slope   → short-term trend
14-day slope  → intermediate trend
30-day slope  → smoother/longer trend
```

At this stage, the slopes are used for **exploratory analysis only**.

No final trend categories are assigned yet.

---

## 5. Slope distribution analysis

The distribution of the rolling slopes was analyzed using descriptive statistics and percentiles.

This analysis showed an important difference between cryptocurrencies.

For example, the 7-day slope distributions have substantially different scales:

```text
Bitcoin       P05 ≈ -0.0123    P95 ≈  0.0164
Ethereum      P05 ≈ -0.0289    P95 ≈  0.0329
Binance Coin  P05 ≈ -0.0143    P95 ≈  0.0159
Ripple        P05 ≈ -0.0147    P95 ≈  0.0233
Tether        P05 ≈ -0.000075  P95 ≈  0.000107
USD Coin      P05 ≈ -0.000019  P95 ≈  0.000018
```

This shows that fixed absolute thresholds for slope would not be appropriate across all cryptocurrencies.

For example, thresholds such as:

```text
-0.20
-0.05
+0.05
+0.20
```

would be too extreme for most of the observed data.

Therefore, the final trend categories will be defined in a later stage using a data-driven approach rather than arbitrary fixed slope values.

The planned trend classes are:

```text
-2 → strong decrease
-1 → decrease
 0 → stable
+1 → increase
+2 → strong increase
```

The exact thresholds will be established during **target definition**, not during the EDA.

---

## 6. Moving averages

Moving averages are calculated using:

```text
MA7
MA30
```

These provide smoothed representations of the price series and help identify changes in short- and medium-term price behavior.

They are also potential candidates for future predictive features.

---

## 7. Time-series decomposition

The price series are decomposed using additive and multiplicative approaches with periods of:

```text
7 days
30 days
```

The decomposition is used as an exploratory tool to inspect:

- trend
- seasonal component
- residuals

The results are not interpreted as definitive evidence of a specific seasonal pattern. In particular, the use of a 7-day period does not by itself establish the existence of weekly seasonality.

---

# EDA Conclusions

The EDA provides several conclusions that will guide the next stages of the project.

### 1. The cryptocurrencies have substantially different behavior

Bitcoin, Ethereum, Binance Coin and Ripple show considerably greater variability than Tether and USD Coin.

Therefore, the modeling stage should account for the different scales and dynamics of each cryptocurrency.

### 2. Returns and volatility are important variables

Price levels alone do not fully describe the behavior of the series. Returns and rolling volatility provide additional information about short-term market dynamics.

### 3. Temporal dependence is present

The autocorrelation analysis provides evidence that the time dimension should be explicitly considered when constructing predictive models.

### 4. Trend depends on the observation window

The 7-, 14- and 30-day slopes capture different levels of trend sensitivity.

Shorter windows respond more quickly to changes, while longer windows provide smoother trend estimates.

### 5. Absolute slope thresholds are not appropriate across cryptocurrencies

The slope distributions differ considerably between assets, particularly between volatile cryptocurrencies and stablecoins.

Consequently, the final trend classification should use thresholds that account for the distribution of the data rather than arbitrary absolute values.

### 6. The EDA is complete

The exploratory analysis provides sufficient information to move to the next stage:

```text
EDA
 ↓
Target Definition
```

The next stage will define the prediction targets and their corresponding horizons.

---

# Planned Prediction Targets

The project will investigate both **price prediction** and **trend prediction**.

The prediction horizons currently considered are:

| Horizon | Period |
|---|---:|
| Short-term | 7 days |
| Medium-term | 21 days |
| Long-term | 50 days |

These horizons are currently treated as the project's working definition and will be implemented and evaluated during the target-definition stage.

### Price prediction

The objective will be to predict future cryptocurrency prices at the selected horizons.

### Trend prediction

The objective will be to classify future price behavior into five categories:

```text
-2 → strong decrease
-1 → decrease
 0 → stable
+1 → increase
+2 → strong increase
```

The precise mathematical definition of these classes will be established in the next notebook.

---

# Next Steps

The next stages of development are:

```text
1. Data acquisition              ✅
2. Preprocessing                 ✅
3. Exploratory Data Analysis     ✅
4. Target definition             → next
5. Feature engineering
6. Dataset creation
7. Model training
8. Model comparison
9. Evaluation
```

Potential modeling approaches will be selected after the targets and features have been defined. Statistical time-series models, machine-learning models and change-point detection methods will be considered according to their suitability for each task.

---

# Data Export

Processed datasets are exported to the `data/processed/` directory using the project's CSV export utility.

The export utility ensures a consistent format for the processed cryptocurrency time series and provides reproducible inputs for subsequent analysis.

---

# Automation

The project includes an automated data pipeline based on **GitHub Actions** and **Supabase**.

The workflow is designed to periodically execute the data acquisition pipeline, retrieve updated cryptocurrency data, and store it in the remote PostgreSQL database.

The local project can also be configured to run the main pipeline using operating-system scheduling tools such as:

- Windows Task Scheduler
- WSL `cron`
- Linux `cron`
- macOS `launchd`

---

## Previous Setup

Until June 2025, the data was manually fetched and stored locally in a SQLite database. This required running scripts manually to update the dataset.

---

## Current Setup

The project now uses Supabase for remote PostgreSQL database hosting and GitHub Actions for scheduled data updates.

### Database Migration

- Data from the local SQLite database was migrated to Supabase PostgreSQL.
- The database schema was synchronized with the remote database.

### Automated Data Fetching and Storage

The automated workflow:

1. Initializes the database schema if required.
2. Fetches the latest cryptocurrency data through the CoinGecko API.
3. Stores the data in the Supabase PostgreSQL database.

### Environment Configuration

Sensitive configuration values are stored outside the repository.

For local development, environment variables are configured using a `.env` file at the project root.
