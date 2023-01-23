import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

plt.rcParams["axes.facecolor"] = "#282828"
plt.rcParams["axes.labelcolor"] = "#EBDBB2"
plt.rcParams["axes.edgecolor"] = "#EBDBB2"
plt.rcParams["figure.facecolor"] = "#282828"
plt.rcParams["grid.color"] = "#EBDBB2"
plt.rcParams["text.color"] = "#EBDBB2"
plt.rcParams["xtick.color"] = "#EBDBB2"
plt.rcParams["ytick.color"] = "#EBDBB2"


def consecutive(window, total, runs):
    """

    Args:
        window: window of elements to look over
        total: current total number of samples viewed
        runs: current number of runs found

    Returns:
        total, runs

    """
    if all(day for day in window[0:-1]):
        if window[-1]:
            return total + 1, runs + 1
        return total + 1, runs
    return total, runs


def sliding_window(elements, window_size, run_function):
    """

    Args:
        elements: elements to apply sliding window to
        window_size: sliding window size
        run_function: function that calculates number of runs

    Returns:
        number of runs and total number of samples taken

    """
    total = 0
    runs = 0
    length = len(elements)
    if length <= window_size:
        return elements
    for idx, _ in enumerate(elements):
        if idx < length - window_size:
            total, runs = run_function(elements[idx : idx + window_size], total, runs)
    return runs, total


def get_results(num_consecutive_days, green_df):
    """

    Args:
        num_consecutive_days: number of days used to calculate a run
        green_df: dataframe marking green days

    Returns:
        chance: chance of a green day after num_consecutive_days of a run

    """
    green_df.dropna(inplace=True)
    runs, total = sliding_window(green_df, num_consecutive_days, consecutive)
    try:
        chance = runs / total
        return chance, runs, num_consecutive_days
    except ZeroDivisionError:
        return 0, 0, 0


ticker_dict = {
    "WMT": None,
    "AMZN": None,
    "AAPL": None,
    "CVS": None,
    "TM": None,
    "VWAGY": None,
}
multi = yf.Tickers(" ".join(ticker_dict.keys()))
df = multi.history("max")
df = df["Close"]

for ticker in ticker_dict:
    df[f"Green {ticker}"] = df[ticker].diff() > 0
    ticker_dict[ticker] = [
        get_results(num, df[f"Green {ticker}"]) for num in range(2, 8)
    ]
