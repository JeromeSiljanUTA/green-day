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

aapl = yf.Ticker("AAPL")

df = aapl.history("max")

df["Green"] = df["Close"].diff() > 0


def consecutive(window, total, runs):
    if all(day for day in window[0:-1]):
        if window[-1]:
            return total + 1, runs + 1
        else:
            return total + 1, runs
    else:
        return total, runs


def sliding_window(elements, window_size):
    total = 0
    runs = 0
    length = len(elements)
    if length <= window_size:
        return elements
    for idx, row in enumerate(elements):
        if idx < length - window_size:
            total, runs = consecutive(elements[idx : idx + window_size], total, runs)
    return runs, total


def show_results(num_consecutive_days):
    runs, total = sliding_window(df["Green"], num_consecutive_days)
    percentage = runs / total
    return percentage, runs
