# **CryptoTrendPredictor**
Predicting temporal tendencies of cryptocurrencies using ML

## **Proyect structure**
``` markdown
/CryptoTrendPredictor/
├── .github/workflows # Folder with all actions for GitHub Actions
|    └── run_main.yml # Script to automatize the data retrieval and data dump to Supabase database

├── data/
|    └── processed/
|    └── raw/
|        ├── crypto_data.db # Local database in SQLite until June
|        └── db_23062025.csv 
│ └── crypto_data.db # SQLite database file (local storage)

├── notebooks/
|    ├── 1-obtain_data.ipynb # Script to obtain data for the local database
|    ├── 2-create_subset.ipynb # Script to select only data for a bitcoin
|    ├── 3-clean_data_binance.ipynb # Script to clean data an imput NAs
|    ├── 4-eda_binance.ipynb
|    ├── 5-features_binance.ipynb # Script to do advanced feature engineering 
|    ├── 6-dataset_creation.ipynb # Split train and test datasets   


├── src/
|    ├── config.py # Script with configuration parameters (e.g., list of cryptocurrencies)
|    ├── database.py # Script to initialize, create tables, and save to the database
|    ├── fetch_data.py # Script to fetch data from the API and save it to the database
|    ├── main.py # Script used for obtain data automatically
|    └── migrate_db.py # Script for migrate from SQLite db to a PostgreSQL
```

## **Overview**  
**CryptoTrendPredictor** is a modular framework designed to analyze and forecast cryptocurrency market trends using both **time series** and **machine learning** techniques.  
It focuses on two main predictive tasks:  

1. **Price Forecasting:** Predicting the *future value* of a cryptocurrency (e.g., USD price).  
2. **Return Forecasting:** Predicting *future returns* or *price direction* (up/down movement).  

The project aims to combine financial indicators, deep learning architectures, and ML-based classifiers to evaluate different modeling approaches for financial time series.


        ┌────────────────────────┐
        │   RAW BINANCE DATA     │
        │  (price, volume, cap)  │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   FEATURE ENGINEERING   │
        │  make_features()        │
        │  → adds RSI, MACD, ...  │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   binance_features.csv  │
        └──────────┬─────────────┘
         ┌─────────┴───────────────┐
         │                         │
         ▼                         ▼
┌────────────────────┐    ┌────────────────────┐
│ PRICE DATASET      │    │ RETURNS DATASET    │
│ target_price = t+1 │    │ target_return = t+1│
│                    │    │ target_class ↑↓    │
└─────────┬──────────┘    └─────────┬──────────┘
          │                         │
          ▼                         ▼
  ┌───────────────┐         ┌────────────────┐
  │ train_price   │         │ train_returns  │
  │ test_price    │         │ test_returns   │
  └──────┬────────┘         └──────┬─────────┘
         │                         │
         ▼                         ▼
┌─────────────────────┐   ┌──────────────────────────┐
│ TIME SERIES MODELS  │   │ ML/DL MODELS (XGB, RF...)│
│ (ARIMA, Prophet...) │   │ Regression / Classification │
└─────────────────────┘   └──────────────────────────┘


## **Data Pipeline**

### **Raw Data**
Raw historical data is collected from Binance and includes features such as:
- `date`
- `price_usd`
- `volume`
- `market_cap`
- `change`

This dataset provides the base for all subsequent feature engineering and modeling tasks.

### **Feature Engineering**
The preprocessing phase transforms raw data into a feature-rich dataset (`binance_features.csv`) by computing:
- **Technical indicators** (RSI, MACD, Bollinger Bands, Moving Averages)  
- **Volatility metrics**  
- **Lagged features and returns**  
- **Temporal encodings** (day of week, month, quarter)

This stage prepares the data for both time series forecasting and supervised ML models.


### **Dataset Creation and Splitting**

From the feature-enhanced data, two separate datasets are generated based on prediction type:

#### **Price Prediction Dataset**
Used for models like **ARIMA, Prophet, and LSTM** that focus on forecasting future price values.

```python
target_price = price_usd.shift(-1)
```

- Predicts the *next-day price*.
- Splits the data chronologically into **80% train** and **20% test** sets.

Output files:
```
binance_target_price.csv
binance_train_price.csv
binance_test_price.csv
```

#### **Returns Prediction Dataset**
Used for **machine learning and deep learning** models that predict *future returns* or *trend direction*.

```python
target_return = returns.shift(-1)
target_class = (target_return > 0).astype(int)
```

- Predicts the *next-day return* (continuous) and *trend class* (binary).  
- Also split temporally (80% / 20%).

Output files:
```
binance_target_returns.csv
binance_train_returns.csv
binance_test_returns.csv
```

## **Modeling Approaches**

| Task Type | Model Family | Example Models | Objective |
|------------|---------------|----------------|------------|
| **Time Series Forecasting** | Statistical / DL | ARIMA, Prophet, LSTM | Predict future **price values** |
| **Machine Learning Regression** | Tree-based / Neural | XGBoost, Random Forest, MLP | Predict **next-day returns** |
| **Classification** | Supervised Learning | Logistic Regression, SVM, LightGBM | Predict **trend direction (up/down)** |

Each model is evaluated using both standard performance metrics (MAE, RMSE, R²) and trading-related measures (accuracy of direction, precision, recall).

## **Data Export**

All generated datasets are automatically saved into the `/data/processed/` directory using the utility function:

```python
export_dataset(df, path, include_index=False)
```

This ensures reproducibility and consistent access to processed data for later experimentation.


-----------



## **Automating ```main.py``` Execution**
To ensure that ```main.py``` runs automatically at regular intervals without manual intervention, follow the appropriate setup based on your operating system.

### **Windows: Task Scheduler**
Windows provides the **Task Scheduler**, which allows you to automate script execution.

Steps to schedule ```main.py``` in Windows:
**CMD**
1. **Open Task Scheduler:**
    Press ```Win + R```, type ```taskschd.msc```, and press ```Enter```.

2. **Create a new task:**
    Click **"Create Basic Task"** on the right panel.

3. **Set task name and description:**
    - Name it something like ```Crypto Data Fetcher```.
    - Add a short description: *Runs main.py to fetch cryptocurrency data*.

4. **Choose the frequency:**
    Select  ```Daily ``` or  ```Hourly ```, depending on how often you want the script to run.

5. **Set the start time:**
    Choose the time and interval for execution.

6. **Select the action → Start a program:**
    - Under "Program/script", enter:

        ```sh
        C:\Windows\System32\cmd.exe
        ```
    - Under **"Add arguments"**, enter the path to ```main.py```:
        ```sh
        /c "C:\path\to\your\project\venv\Scripts\activate && python C:\path\to\your\project\main.py"
        ```
    - Under **"Start in"**, enter the folder where ```main.py``` is located.
    ```sh
    C:\path\to\your\project
    ```

7. **Finish and save:**
    Confirm and test the scheduled task.

The Task Scheduler will now run ```main.py``` at the specified intervals.

**WSL**
1. **Open WSL Terminal:**

2. **Edit the crontab file:**
    ```sh
    crontab -e
    ```

3. **Add the following cron job to run main.py every hour:**
    ```Hourly```
    ```sh
    0 * * * * source /mnt/c/Users/YOUR_USER/path/to/venv/Scripts/activate && python /mnt/c/Users/YOUR_USER/path/to/main.py
    ```

    ```Daily``` <!-- Runs at 03:00 AM -->
    ```sh
    0 3 * * * source /mnt/c/Users/YOUR_USER/path/to/venv/Scripts/activate && python /mnt/c/Users/YOUR_USER/path/to/main.py
    ```
    (Replace ```YOUR_USER``` with your username and update the script path accordingly.)

4. **Save and exit:**
    In nano, press ```Ctrl + X```, then ```Y```, and ```Enter```.

5. **Check scheduled jobs:**
    ```sh
    crontab -l
    ```

Possibily, WSL does not execute ```cron``` automatically, but you can configure:
1. **Open WSL configuration file:**
    ```sh
    sudo nano /etc/wsl.conf
    ```

2. **Add at the end of the file:**
    ```markdown
    [boot]
    command="service cron start"
    ```

3. **Save and restart the terminal:**
    ```sh
    wsl --shutdown
    ```

- To check if ```cron``` is running:
    ```sh
    sudo service cron status
    ```

- To iniziate ```cron```:
    ```sh
    sudo service cron start
    ```

- To check if ```cron jobs``` are been executed:
    ```sh
    grep cron /var/log/syslog
    ```



### **Mac: Using ```launchd``` (LaunchAgents)**
On macOS, you can automate tasks using ```launchd``` by creating a **LaunchAgent**.

Steps to automate main.py in macOS:
1. **Open Terminal:**
    Press ```Cmd + Space```, type ```Terminal```, and press ```Enter```.

2. **Create a new LaunchAgent configuration file:**
    ```sh
    nano ~/Library/LaunchAgents/com.crypto.fetch.plist
    ```

3. **Add the following configuration:**
    ```Hourly ```
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.crypto.fetch</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>/Users/YOUR_USER/path/to/project/main.py</string>
            </array>
            <key>StartInterval</key>
            <integer>3600</integer> <!-- Runs every 3600 seconds (1 hour) -->
            <key>RunAtLoad</key>
            <true/>
        </dict>
    </plist>
    ```

    ```Daily ```
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.crypto.fetch</string>
            <key>ProgramArguments</key>
            <array>
                <string>/usr/bin/python3</string>
                <string>/Users/YOUR_USER/path/to/project/main.py</string>
            </array>
            <key>StartCalendarInterval</key>
            <dict>
                <key>Hour</key>
                <integer>3</integer> <!-- Runs at 03:00 AM -->
                <key>Minute</key>
                <integer>0</integer>
            </dict>
            <key>RunAtLoad</key>
            <true/>
        </dict>
    </plist>
    ```

    (Replace ```YOUR_USER``` with your actual username and update the ```main.py``` path accordingly.)

4. **Load the task into ```launchd```:**
    ```sh
    launchctl load ~/Library/LaunchAgents/com.crypto.fetch.plist
    ```
    ```launchd``` will now automatically run ```main.py``` every hour.

    To verify if it is running:
    ```sh
    launchctl list | grep com.crypto.fetch
    ```



### **Linux: Using ```cron``` Jobs:**
In Linux, we can use ```cron```, a built-in task scheduler.

Steps to automate ```main.py``` in Linux:
1. **Open Terminal:**
    Press ```Ctrl + Alt + T```.

2. **Edit the crontab file:**
    ```sh
    crontab -e
    ```

3. **Add the following cron job to run main.py every hour:**
    ```Hourly```
    ```sh
    0 * * * * /bin/bash -c 'source /home/YOUR_USER/path/to/project/venv/bin/activate && python /home/YOUR_USER/path/to/project/main.py'
    ```

    ```Daily``` <!-- Runs at 03:00 AM -->
    ```sh
    0 3 * * * /bin/bash -c 'source /home/YOUR_USER/path/to/project/venv/bin/activate && python /home/YOUR_USER/path/to/project/main.py'
    ```
    (Replace ```YOUR_USER``` with your username and update the script path accordingly.)

4. **Save and exit:**
    In nano, press ```Ctrl + X```, then ```Y```, and ```Enter```.

5. **Check scheduled jobs:**
    ```sh
    crontab -l
    ```

Now, ```cron``` will automatically run main.py every hour.


## Previous Setup

Until June 2025, the data was manually fetched and stored locally in a SQLite database. This required running scripts manually to update the dataset.

---

## Current Setup (since 23rd June 2025)

To automate data fetching, storage, and migration, the project now integrates with **Supabase** for remote PostgreSQL database hosting and uses **GitHub Actions** for scheduling daily data updates.

### Database Migration

- Data from the local SQLite database is migrated to Supabase PostgreSQL.
- Database schema is synchronized with the remote database.

### Automated Data Fetching and Storage

- A scheduled GitHub Actions workflow runs daily at **12:00 PM CET** (10:00 UTC).
- The workflow runs `src/main.py` which:
  - Initializes the database schema if needed.
  - Fetches the latest cryptocurrency data from the CoinGecko API.
  - Stores the data in the Supabase PostgreSQL database.

### Environment Configuration

- Sensitive information like database connection URLs are stored in GitHub Secrets as `POSTGRES_URL`.
- The project uses a `.env` file at the project root for local development.

---

## How to Run Locally

1. Create and configure your `.env` file in the project root with the following:

   ```env
   POSTGRES_URL=postgresql://username:password@host:port/database

