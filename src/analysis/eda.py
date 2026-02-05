# Script with EDA functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


def split_train_test(df: pd.DataFrame, threshold: float = 0.8):

    '''
    Split datasets in X_train, y_train, X_test and y_test

    Parameters:
    df (pd.DataFrame): a dataframe
    threshold: the percentage of original data intended for train subdataset. By default, 80% of data are inteded fir train subset

    Returns:
    Four pd.DataFrame
    '''
    
    lengt_df = df.shape[0]
    threshold_df = int(lengt_df*threshold)

    train = df.iloc[: threshold_df]
    test = df.iloc[threshold_df :]


    return train, test



def time_plots(df: pd.DataFrame, features: list | None = None) -> None:

    '''
    Display subplot of temporal variables.

    Parameter:
        - df: pd.DataFrame
        - features: a list. By default: None

    Returns:
        - None
    '''
    fig, ax = plt.subplots(len(features), 1, figsize = (10, 6), sharex = True) #sharex = True is for sahering 
    # x axis

    for i, var in enumerate(features):
        ax[i].plot(df['date'], df[var], label = var)
        ax[i].legend(loc = "upper right")
        ax[i].set_ylabel(var)

    # for the last subplot
    ax[-1].set_xlabel("Date")

    plt.tight_layout() # Avoid overlapping
    plt.show()



def matrix_correlation(df: pd.DataFrame, features: list | None = None) -> None:

    '''
    Display a correlation matrix.

    Parameters:
        - df: pd.DataFrame
        - features: a list. By default: None

    Returns:
        - None
    '''
    corr_matrix = df[features].corr()

    plt.figure(figsize=(6,4))
    sns.heatmap(corr_matrix, annot=True, cmap='vlag', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Correlation matrix")
    plt.show()



def scatter_matrix(df: pd.DataFrame, features: list | None = None) -> None:
    '''
    Display distribution of a feature and scatter plots between features.

    Parameters:
        - df: pd.DataFrame
        - features: a list. By default: None

    Returns:
        - None
    '''
    if features is None:
        features = ['price_usd', 'market_cap', 'volume']

    sns.pairplot(df[features], diag_kind="kde", corner=True)
    plt.suptitle("Relaciones entre Price, Market Cap y Volume", y=1.02)
    plt.show()


def decompose_time_series(df: pd.DataFrame, column: str, model: str = "multiplicative", 
                          freq: int = None) -> None:
    '''
    Decompose a temporal serie in tendency, seasional and residuals.
    
    Parameters:
        - df: a Dataframe with a datetime index
        - columns: name of the feature for analysing
        - model: 'additive' or 'multiplicative'. 
            - Additive: tendency and seasonality don't depend on the level of the serie (the value)
                Serie = Tendency + Seasonality + Residuals
            - Multiplicative: tendency ans seasonality depends on the level of teh series (the value)
                Serie = Tendency * Seasonality * Residuals
        - freq: periodicity. By deafault: None. If you want a week: 7. A month: 30

    Returns:
        - DataFrame (copy) with new columns ['returns', 'volatility']
    '''
    # asegurarse de que el índice es datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("Dataframe must have a DatetimeIndex.")
    
    serie = df[column].dropna()

    decomposition = seasonal_decompose(df[column], model=model, period=freq)

    fig = decomposition.plot()
    fig.set_size_inches(10, 8)
    plt.suptitle(f"Descomposición de la serie: {column}", fontsize=14)
    plt.show()



def returns_and_volatility(df: pd.DataFrame, price_col: str = "price_usd", window: int = 7) -> pd.DataFrame:

    '''
    Calculate daily returns (%) and mobile volatibility from a price serie
    
    Paremeters:
        - df: DataFrame con datetime index
        - price_col: name of the column with the price. By default: price_usd
        - window: windows size for volatility (unids: days). By default: 7 days
    
    Returns:
        - DataFrame con nuevas columnas ['returns', 'volatility']
    '''
    
    # Aseguramos orden temporal
    df = df.sort_index().copy()
    
    # Retornos diarios (%)
    df['returns'] = df[price_col].pct_change() * 100
    
    # Volatilidad móvil (rolling std de retornos)
    df['volatility'] = df['returns'].rolling(window=window).std()
    
    # Gráficos
    plt.figure(figsize=(12,6))
    
    # Retornos
    plt.subplot(2,1,1)
    plt.plot(df.index, df['returns'], color='blue', alpha=0.6)
    plt.title(f"Retornos diarios (%) - {price_col}")
    plt.axhline(0, color='black', linewidth=0.8, linestyle="--")
    
    # Volatilidad
    plt.subplot(2,1,2)
    plt.plot(df.index, df['volatility'], color='red')
    plt.title(f"Volatilidad móvil ({window} días)")
    
    plt.tight_layout()
    plt.show()
    
    return df



