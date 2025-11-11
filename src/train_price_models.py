'''
train_price_models.py
---------------------
Core training module for price prediction models.
Includes:
- RandomForest
- XGBoost
- ARIMA
- SARIMA
- Prophet
- Ruptures (structural break detection)

Each function returns (predictions, trained_model).
All models use default hyperparameters for the initial benchmark.
'''

import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Union

from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
import ruptures as rpt


# ====================================================
# MACHINE LEARNING MODELS
# ====================================================

def run_random_forest(X_train: pd.DataFrame,
                      X_test: pd.DataFrame,
                      y_train: pd.Series) -> Tuple[np.ndarray, RandomForestRegressor]:
    
    '''
    Train a Random Forest regressor with default parameters.
    
    Parameters:
        - X_train: a dataframe with features for training
        - X_test: a dataframe with features for evaluation
        - y_train: a dataframe with teh variable to predict

    Returns:
        - y_pred: predictions for X_test and 
        - model: the fitted model.
    '''

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred, model


def run_xgboost(X_train: pd.DataFrame,
                X_test: pd.DataFrame,
                y_train: pd.Series) -> Tuple[np.ndarray, XGBRegressor]:
    '''
    Train a Random Forest regressor with default parameters.
    
    Parameters:
        - X_train: a dataframe with features for training
        - X_test: a dataframe with features for evaluation
        - y_train: a dataframe with teh variable to predict

    Returns:
        - y_pred: predictions for X_test and 
        - model: the fitted model.
    '''

    model = XGBRegressor(random_state=42, n_estimators=200)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred, model


# ====================================================
# 🔹 TIME SERIES MODELS (ARIMA, SARIMA, PROPHET)
# ====================================================

def run_arima(train_series: pd.Series,
              test_len: int = 14) -> Tuple[np.ndarray, ARIMA]:
    '''
    Train an ARIMA model for univariate time series forecasting.

    Parameters:
        - train_series: a pandas Series containing the training time series
        - test_len: number of future steps to forecast (default=14)

    Returns:
        - forecast: array with predicted values for the specified horizon
        - fitted: the fitted ARIMA model
    '''
    model = ARIMA(train_series, order=(1, 1, 1))
    fitted = model.fit()
    forecast = fitted.forecast(steps=test_len)
    return forecast, fitted


def run_sarima(train_series: pd.Series,
               test_len: int = 14) -> Tuple[np.ndarray, SARIMAX]:
    '''
    Train a SARIMA model for seasonal time series forecasting.

    Parameters:
        - train_series: a pandas Series containing the training time series
        - test_len: number of future steps to forecast (default=14)

    Returns:
        - forecast: array with predicted values for the specified horizon
        - fitted: the fitted SARIMA model
    '''
    model = SARIMAX(train_series, order=(1, 1, 1),
                    seasonal_order=(1, 1, 1, 7))
    fitted = model.fit(disp=False)
    forecast = fitted.forecast(steps=test_len)
    return forecast, fitted


def run_prophet(df: pd.DataFrame,
                horizon: int = 14) -> Tuple[pd.DataFrame, Prophet]:
    '''
    Train a Prophet model for time series forecasting.

    Parameters:
        - df: a dataframe with columns ['ds', 'y'] where:
              'ds' = datestamps (datetime)
              'y'  = values to forecast
        - horizon: number of future days to forecast (default=14)

    Returns:
        - forecast: a dataframe with Prophet forecast results
        - model: the fitted Prophet model
    '''
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)
    return forecast, model


# ====================================================
# 🔹 STRUCTURAL BREAK DETECTION (RUPTURES)
# ====================================================

def run_ruptures(price_series: pd.Series,
                 model_name: str = "rbf",
                 n_bkps: int = 5) -> Tuple[List[int], rpt.Pelt]:
    '''
    Detect structural breaks in a time series using the Ruptures library.

    Parameters:
        - price_series: a pandas Series of values to analyze
        - model_name: cost function to use ('rbf', 'l2', 'normal', etc.)
        - n_bkps: maximum number of breakpoints to detect (default=5)

    Returns:
        - breakpoints: list of indices representing detected breakpoints
        - algo: the fitted Ruptures PELT algorithm instance
    '''
    algo = rpt.Pelt(model=model_name).fit(price_series.values)
    breakpoints = algo.predict(pen=10)
    return breakpoints, algo


# ====================================================
# 🔹 EVALUATION
# ====================================================

def evaluate_model(y_true: Union[np.ndarray, pd.Series],
                   y_pred: Union[np.ndarray, pd.Series],
                   model_name: str = "") -> Dict[str, float]:
    '''
    Compute basic regression performance metrics: MAE, RMSE, and R².

    Parameters:
        - y_true: true values
        - y_pred: predicted values
        - model_name: optional string label for the model being evaluated

    Returns:
        - metrics: dictionary containing MAE, RMSE, and R² scores
    '''
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f'📊 {model_name} - MAE: {mae:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f}')
    return {'model': model_name, 'MAE': mae, 'RMSE': rmse, 'R2': r2}


# ====================================================
# 🔹 DEMO USAGE (if run directly)
# ====================================================

if __name__ == '__main__':
    np.random.seed(42)
    X_train = pd.DataFrame(np.random.rand(100, 5))
    X_test = pd.DataFrame(np.random.rand(20, 5))
    y_train = pd.Series(np.random.rand(100))
    y_test = pd.Series(np.random.rand(20))

    # RandomForest
    y_pred_rf, model_rf = run_random_forest(X_train, X_test, y_train)
    evaluate_model(y_test, y_pred_rf, 'RandomForest')

    # XGBoost
    y_pred_xgb, model_xgb = run_xgboost(X_train, X_test, y_train)
    evaluate_model(y_test, y_pred_xgb, 'XGBoost')
