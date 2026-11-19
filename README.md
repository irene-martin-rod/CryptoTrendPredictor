# CryptoTrendPredictor

Predicting cryptocurrency price and trend dynamics using time-series analysis and machine learning.

## Project structure

```text
/CryptoTrendPredictor/
├── .github/
│   └── workflows/
│       └── run_main.yml              # GitHub Actions workflow for automated data updates
├── config/
│   └── preprocess.yaml               # Preprocessing configuration
├── data/
│   ├── processed/
│   │   ├── binancecoin.csv
│   │   ├── bitcoin.csv
│   │   ├── ethereum.csv
│   │   ├── ripple.csv
│   │   ├── tether.csv
│   │   └── usd-coin.csv
│   └── raw/
│       ├── crypto_data.db             # Local SQLite database
│       └── db_04022026.csv            # Raw dataset
├── notebooks/
│   ├── 1-obtain_data.ipynb            # Data acquisition and preprocessing
│   ├── 2-eda_crypto_*.ipynb           # Exploratory Data Analysis for each cryptocurrency
│   └── 3-target_definition.ipynb      # Forecast target design and validation
├── src/
│   ├── analysis/
│   │   └── eda.py                     # EDA and time-series analysis functions
│   ├── preprocess/
│   │   ├── __init__.py
│   │   ├── clean_prices.py            # Price cleaning and missing-price handling
│   │   ├── clean.py                   # Data cleaning and missing-date handling
│   │   ├── export.py                  # CSV export utilities
│   │   ├── run_pipeline.py            # Preprocessing pipeline
│   │   └── split_crypto.py            # Split data by cryptocurrency
│   ├── config.py                      # Configuration parameters
│   ├── database.py                    # Database initialization and storage
│   ├── fetch_data.py                  # Cryptocurrency data acquisition
│   ├── load_supabase_api.py           # Data loading from Supabase
│   ├── main.py                        # Main automated pipeline
│   ├── migrate_db.py                  # SQLite → PostgreSQL migration
│   └── supabase_client.py             # Supabase/PostgreSQL connection
```

# Overview

**CryptoTrendPredictor** is a modular project for analyzing cryptocurrency time series and developing models to predict future price behavior and market trends.

The project maintains processed datasets for six cryptocurrencies:
- Bitcoin
- Ethereum
- Binance Coin
- Ripple
- Tether
- USD Coin

The target-definition experiment described below uses five of these assets. Ripple remains in the processed data and was included in the exploratory analysis, but it is excluded from the current target-definition experiment because its price series presented resolution/stale-value issues that could make the resulting labels unreliable.

The project is divided into several stages:

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

Data acquisition, preprocessing and exploratory data analysis have been completed. The initial target-definition experiment has also been implemented. The next stage is feature engineering.

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

TThe evolution of the following variables is analyzed over time:

- `price_usd`
- `market_cap`
- `volume`

is analyzed over time.

The analysis shows two broad behavioral groups.

### Volatile cryptocurrencies

- Bitcoin
- Ethereum
- Binance Coin
- Ripple

These assets show considerably larger price movements and more variability.

### Stable cryptocurrencies

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

The exploratory analysis provides sufficient information to move from understanding the data to defining the future outcomes that the models will predict.

---

# Target definition
The target-definition stage is implemented in `notebooks/3-target_definition.ipynb`. Its purpose is to translate the forecasting objectives into measurable future outcomes that can later be used as supervised-learning targets.

The notebook does not simply assign trend labels from the current slope. Instead, it defines each target using price observations that occur after the prediction date. This makes the target represent the outcome over a specified future horizon.

## 1. Forecast horizons
Three forecast horizons are considered:

| **Horizon** | **Number of days** |	**Intended interpretation**|
| --- | --- | --- |
| **Short-term** | 7 | Near-future behavior |
| **Medium-term** | 21 | Intermediate behavior |
| **Long-term** | 50 | Longer forecast window |

The same horizons are used for the volatile-cryptocurrency and stablecoin experiments. This makes it possible to study how the prediction task changes as the forecast window becomes longer.

## 2. Asset selection and separate target tasks
The target-definition experiment uses five cryptocurrencies, divided into two groups:

**Volatile cryptocurrencies**
- Bitcoin (bitcoin)
- Ethereum (ethereum)
- Binance Coin (binancecoin)

**Stable cryotocurrencies**
- Tether (tether)
- USD Coin (usd-coin)

Ripple is not included in this experiment. Although it remains in `data/processed/` and was included in EDA, its price series showed price-resolution/stale-value issues. Including it in the current experiment could produce misleading target labels.

The two groups require different definitions:
- For volatile cryptocurrencies, the relevant outcome is the direction and magnitude of the future price return.
- For stable crytocurrencies, the relevant outcome is whether the price departs from its USD 1 peg beyond a small tolerance at any point in the forecast window.


Applying the same trend classes to both groups would not be meaningful. A small stablecoin price movement and a comparable percentage movement in a volatile cryptocurrency represent different prediction problems.

## 3. Future prices and returns
For each observation date \(d\) and forecast horizon \(h\), the notebook obtains the price at the end of the horizon using a negative shift:

```python
future_price = price_usd.shift(-h)
```

The corresponding future return is calculated as:

$$
R_{d,h} = \frac{P_{d+h}}{P_d} - 1
$$

where:

- $P_d$ is the price on the current observation date.
- $P_{d+h}$ is the price after $h$ days.
- $R_{d,h}$ is the future return expressed as a decimal fraction.

For example, a return of 0.05 represents a 5% increase, while -0.05 represents a 5% decrease.

These future prices and returns are used to construct the labels. They must not be included among the model input features: doing so would expose information from the future and cause data leakage.

The target columns for the volatile-asset returns follow the naming pattern:

```text
trend_return_3_7d
trend_return_3_21d
trend_return_3_50d
```

## 4. Chronological train/test separation and leakage prevention
The data is split chronologically, using the first 80% of observations for training and the final 20% for testing. The observations are not shuffled because the temporal order must be preserved.

A further restriction is applied when creating the training target datasets. A training observation is retained only if the end of its future target window occurs strictly before the beginning of the test period.

This is important because a training label must not use a price observation that belongs to the test period. The longest horizon (50 days) determines the largest potential overlap, so the restriction must account for that horizon as well.

The notebook keeps the test data in separate `test_dfs` objects. The final target labels are currently constructed for the training target datasets; the test datasets remain separate at this stage.

The future-derived columns are target-construction data, not model features. Any later feature-engineering or dataset-creation step must preserve this separation.

## 5. Daily continuity requirement
The target calculations use shifts measured in rows. Therefore, `shift(-7)` means seven rows ahead, not automatically seven calendar days ahead.

For the horizons to represent 7, 21 and 50 calendar days, the processed series must have a continuous daily index with no missing dates. The notebook checks date continuity as part of target construction.

This check is important: without a continuous daily series, a row-based shift could refer to a different calendar interval and the target would no longer represent the intended horizon.

## 6. Volatile cryptocurrencies: three-class future-return target
For Bitcoin, Ethereum and Binance Coin, the notebook defines a three-class target from the future percentage return.

The classes are:

| **Label** |	**Meaning** |	**Condition** |
| --- | --- | --- |
| **-1** | Downward | Future return is at or below the negative threshold |
| **0** | Sideways  | Future return is between the two thresholds |
| **+1** | Upward  | Future return is at or above the positive threshold |

The thresholds depend on the forecast horizon:

| **Horizon** | **Downward threshold** | **Upward threshold** |
| --- | --- | --- |
| **7 days** | -3% |	+3% |
| **21 days** | -5% | +5% |
| **50 days** | -8% | +8% |

In other words, the short-term target uses a narrower return band, while the longer horizons use wider bands. This reflects the fact that larger cumulative movements become more plausible over longer periods.

The classification is based on the future return, not on the current rolling slope. The slope analysis in EDA helped establish that a common absolute slope threshold would not work well across assets, but the final volatile-asset target uses percentage-return thresholds.

Earlier possibilities included a five-class trend definition and volatility-normalized approaches. These were not selected for the current implementation. The notebook uses three classes because the chosen task focuses on distinguishing meaningful downward, sideways and upward future outcomes.

The target columns are named:

```text
trend_return_3_7d
trend_return_3_21d
trend_return_3_50d
```

The notebook also examines the resulting class distributions. This is necessary to understand whether the chosen thresholds produce usable numbers of observations in each class and whether the classes are imbalanced. Class distributions should be reviewed again on the final training dataset before model selection.

## 7. Stablecoins: future peg-deviation event
For Tether and USD Coin, predicting upward or downward trends using the same thresholds as volatile cryptocurrencies would not describe the most relevant behavior. Their intended value is close to USD 1, so the target instead measures whether the peg is exceeded by a specified tolerance during the forecast window.

A simple comparison between the current price and the price at the end of the horizon would miss temporary deviations that occur and recover before the final day. To avoid that limitation, the notebook examines every daily price inside the future window.

For a current date \(d\) and horizon \(h\), the maximum absolute deviation is:

```text
\[
\text{Max deviation (\%)} =
100 \times \max_{1 \leq t \leq h}
\left|P_{d+t} - 1\right|
\]

The calculation:
- excludes the current day's price;
- considers all future daily prices from day 1 through day \(h\);
- measures the absolute distance from USD 1;
- keeps the largest deviation observed in that window.
```

The selected tolerance is:

```python
PEG_TOLERANCE = 0.02  # percent
```

The binary target is defined as follows:
| **Label** |	**Meaning** |	**Condition** |
| --- | --- | --- |
| **0** | Within tolerance | Maximum deviation is less than or equal to 0.02% |
| **1** | Deviation event |	Maximum deviation is greater than 0.02% |

The notebook creates the following columns:
```text
max_peg_deviation_7d
max_peg_deviation_21d
max_peg_deviation_50d

target_peg_7d
target_peg_21d
target_peg_50d
```

This definition detects whether a price deviation beyond the selected tolerance occurs at least once during the horizon. It does not measure the duration of the deviation, and it does not by itself establish that a severe or economically significant depeg has occurred.

The 0.02% tolerance is an experimental threshold chosen for this project. It should not be interpreted as a universal definition of a stablecoin depeg. The class distributions and the sensitivity of the results to this threshold should be considered during later evaluation.

A label is only defined when the complete future window is available. If the dataset ends before all \(h\) future observations exist, the corresponding target remains undefined (NaN) rather than being assigned a negative label. This prevents incomplete windows from being incorrectly treated as evidence that no deviation occurred.

## 8. Target-definition conclusions
The notebook establishes two different supervised-learning tasks:

1. **Volatile-asset direction classification:** predict whether Bitcoin, Ethereum or Binance Coin will have a sufficiently negative, small, or sufficiently positive return over 7, 21 or 50 days.
2. **Stable peg-deviation classification:** predict whether Tether or USD Coin will exceed the selected maximum-deviation tolerance at any point during the corresponding future window.

The main decisions and their rationale are:

- **Different target definitions by asset type:** volatile assets and stablecoins have different objectives and price dynamics, so one shared classification rule would not be appropriate.
- **Future returns for volatile assets:** percentage returns express price movement relative to the current price and are more comparable across assets than absolute price changes.
- **Three classes for volatile assets:** the current experiment distinguishes downward, sideways and upward outcomes rather than using the earlier five-class proposal.
- **Horizon-dependent thresholds:** the return bands become wider for longer forecast horizons.
- **Maximum in-window deviation for stable cryptocurrencies:** checking all future prices captures temporary peg deviations that an endpoint-only comparison could miss.
- **Complete future windows only:** incomplete horizons are left undefined to avoid incorrect labels.
- **Chronological splitting and a training-window boundary:** these preserve temporal order and prevent training labels from reaching into the test period.

These targets are working definitions for the current experiment. They are not claims that the selected thresholds are universal market boundaries. Their usefulness must be assessed through class-distribution analysis, model evaluation and sensitivity checks.

---

# Next Steps

The next stages of development are:

```text
1. Data acquisition              ✅
2. Preprocessing                 ✅
3. Exploratory Data Analysis     ✅
4. Target definition             ✅ (initial experiment)
5. Feature engineering           → next
6. Dataset creation
7. Model training
8. Model comparison
9. Evaluation
```

Feature engineering will create explanatory variables using information available on or before each prediction date. Future-derived prices, returns, maximum deviations and target labels must remain excluded from the input features.

Potential modeling approaches will be selected after the feature set and final training datasets have been defined. Statistical time-series models and machine-learning models will be considered according to their suitability for each prediction task.

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
