# EDA functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


def split_train_test(df: pd.DataFrame, threshold: float = 0.8):
    """Split a time series chronologically into train and test datasets."""
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1.")

    df = df.sort_index().copy()
    split_idx = int(len(df) * threshold)
    return df.iloc[:split_idx].copy(), df.iloc[split_idx:].copy()


def time_plots(df: pd.DataFrame, features: list | None = None) -> None:
    """Display temporal plots for selected features."""
    if features is None:
        features = ["price_usd", "market_cap", "volume"]
    if not features:
        raise ValueError("features cannot be empty.")

    fig, axes = plt.subplots(len(features), 1, figsize=(10, 6), sharex=True)
    if len(features) == 1:
        axes = [axes]

    x = df.index if isinstance(df.index, pd.DatetimeIndex) else df["date"]

    for ax, var in zip(axes, features):
        ax.plot(x, df[var], label=var)
        ax.legend(loc="upper right")
        ax.set_ylabel(var)
        ax.grid(alpha=0.2)

    axes[-1].set_xlabel("Date")
    plt.tight_layout()
    plt.show()


def matrix_correlation(df: pd.DataFrame, features: list | None = None) -> None:
    """Display a correlation matrix for selected features."""
    if features is None:
        features = ["price_usd", "market_cap", "volume"]

    corr_matrix = df[features].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        corr_matrix, annot=True, cmap="vlag", fmt=".2f",
        linewidths=0.5, vmin=-1, vmax=1
    )
    plt.title("Correlation matrix")
    plt.tight_layout()
    plt.show()


def scatter_matrix(df: pd.DataFrame, features: list | None = None) -> None:
    """Display distributions and pairwise relationships."""
    if features is None:
        features = ["price_usd", "market_cap", "volume"]

    sns.pairplot(df[features], diag_kind="kde", corner=True)
    plt.suptitle("Relationships between Price, Market Cap and Volume", y=1.02)
    plt.show()


def decompose_time_series(
    df: pd.DataFrame,
    column: str,
    model: str = "multiplicative",
    freq: int = 7,
) -> None:
    """Decompose a time series into trend, seasonality, and residuals."""
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a DatetimeIndex.")
    if model not in {"additive", "multiplicative"}:
        raise ValueError("model must be 'additive' or 'multiplicative'.")
    if freq is None or freq < 2:
        raise ValueError("freq must be an integer >= 2.")

    series = df[column].dropna()
    if len(series) < 2 * freq:
        raise ValueError(f"At least {2 * freq} observations are required.")
    if model == "multiplicative" and (series <= 0).any():
        raise ValueError("Multiplicative decomposition requires positive values.")

    decomposition = seasonal_decompose(series, model=model, period=freq)
    fig = decomposition.plot()
    fig.set_size_inches(10, 8)
    fig.suptitle(
        f"Time-series decomposition: {column} ({model}, period={freq})",
        fontsize=14,
    )
    plt.tight_layout()
    plt.show()


def returns_and_volatility(
    df: pd.DataFrame, price_col: str = "price_usd", window: int = 7
) -> pd.DataFrame:
    """Calculate percentage returns and rolling volatility."""
    if window < 2:
        raise ValueError("window must be >= 2.")

    result = df.sort_index().copy()
    result["returns"] = result[price_col].pct_change() * 100
    result["volatility"] = result["returns"].rolling(window=window).std()

    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    axes[0].plot(result.index, result["returns"], alpha=0.6)
    axes[0].axhline(0, linewidth=0.8, linestyle="--")
    axes[0].set_title(f"Daily returns (%) - {price_col}")
    axes[0].set_ylabel("%")
    axes[0].grid(alpha=0.2)

    axes[1].plot(result.index, result["volatility"])
    axes[1].set_title(f"Rolling volatility ({window} days)")
    axes[1].set_ylabel("Volatility")
    axes[1].set_xlabel("Date")
    axes[1].grid(alpha=0.2)

    plt.tight_layout()
    plt.show()
    return result


def trend_slope(
    df: pd.DataFrame,
    price_col: str = "price_usd",
    window: int = 7,
    use_log: bool = True,
) -> pd.DataFrame:
    """
    Calculate rolling linear-regression slope.

    By default the regression is performed on log(price), making the
    slope comparable across cryptocurrencies with different price scales.
    """
    if window < 2:
        raise ValueError("window must be >= 2.")

    result = df.sort_index().copy()
    values = result[price_col].astype(float)

    if use_log:
        if (values <= 0).any():
            raise ValueError("Log-price requires strictly positive prices.")
        values = np.log(values)

    x = np.arange(window, dtype=float)

    def calculate_slope(y):
        if np.isnan(y).any():
            return np.nan
        return np.polyfit(x, y, 1)[0]

    result["trend_slope"] = values.rolling(window).apply(
        calculate_slope, raw=True
    )

    if use_log:
        result["trend_slope_pct"] = (
            np.exp(result["trend_slope"]) - 1
        ) * 100
    else:
        result["trend_slope_pct"] = (
            result["trend_slope"] / result[price_col]
        ) * 100

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    axes[0].plot(result.index, result[price_col])
    axes[0].set_title(f"Price - {price_col}")
    axes[0].set_ylabel("Price")
    axes[0].grid(alpha=0.2)

    axes[1].plot(result.index, result["trend_slope_pct"])
    axes[1].axhline(0, linewidth=0.8, linestyle="--")
    axes[1].set_title(f"Trend slope ({window} days)")
    axes[1].set_ylabel("Approx. %/day")
    axes[1].set_xlabel("Date")
    axes[1].grid(alpha=0.2)

    plt.tight_layout()
    plt.show()
    return result


def moving_averages(
    df: pd.DataFrame,
    price_col: str = "price_usd",
    windows: tuple = (7, 30),
) -> pd.DataFrame:
    """Calculate and plot rolling moving averages."""
    result = df.sort_index().copy()

    for window in windows:
        if window < 2:
            raise ValueError("Moving-average windows must be >= 2.")
        result[f"ma_{window}d"] = result[price_col].rolling(window).mean()

    plt.figure(figsize=(12, 5))
    plt.plot(result.index, result[price_col], label=price_col)
    for window in windows:
        plt.plot(result.index, result[f"ma_{window}d"], label=f"MA {window}d")

    plt.title("Price and moving averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()
    return result


def autocorrelation_plots(
    df: pd.DataFrame,
    columns: list | None = None,
    lags: int = 30,
) -> None:
    """Plot autocorrelation for selected series."""
    from statsmodels.graphics.tsaplots import plot_acf

    if columns is None:
        columns = ["price_usd", "returns"]

    for column in columns:
        series = df[column].dropna()
        if len(series) <= lags:
            raise ValueError(f"Not enough observations for {lags} lags.")

        fig, ax = plt.subplots(figsize=(10, 4))
        plot_acf(series, lags=lags, ax=ax)
        ax.set_title(f"Autocorrelation: {column}")
        plt.tight_layout()
        plt.show()


def slope_distribution(
    df: pd.DataFrame,
    price_col: str = "price_usd",
    windows: tuple = (7, 14, 30),
) -> pd.DataFrame:
    """
    Calculate rolling log-price slopes and summarize their distributions.

    Returns a DataFrame with descriptive statistics and selected percentiles
    for each slope window.
    """
    result = {}

    for window in windows:
        slope_df = trend_slope(df, price_col=price_col, window=window)

        slope = slope_df["trend_slope"].dropna()

        result[f"slope_{window}"] = {
            "count": slope.count(),
            "min": slope.min(),
            "p05": slope.quantile(0.05),
            "p10": slope.quantile(0.10),
            "p25": slope.quantile(0.25),
            "median": slope.median(),
            "p75": slope.quantile(0.75),
            "p90": slope.quantile(0.90),
            "p95": slope.quantile(0.95),
            "max": slope.max(),
            "mean": slope.mean(),
            "std": slope.std(),
        }

    summary = pd.DataFrame(result).T

    return summary
