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

df = df[["Close"]]
df["Green"] = df["Close"].diff() > 0


def three_green(window, total, fourth):
    if window[0] & window[1] & window[2]:
        if window[3]:
            return total + 1, fourth + 1
        else:
            return total + 1, fourth
    else:
        return total, fourth


def sliding_window(elements, window_size):
    total = 0
    fourth = 0
    length = len(elements)
    if length <= window_size:
        return elements
    for idx, row in enumerate(elements):
        if idx < length - window_size:
            total, fourth = three_green(
                elements[idx : idx + window_size], total, fourth
            )
    return fourth, total


fourth, total = sliding_window(df["Green"], 4)

print(f"Total number of 3 green days in a row: {total}")
print(f"Total number of 4th green day given 3 green days in a row: {fourth}")
print(f"Percentage: {fourth/total}")

pie_df = pd.DataFrame({"total": [total], "fourth": [fourth]})

data = [fourth, total - fourth]
keys = ["True", "False"]
plt.title("Green day given as 4th consecutive green day")
plt.pie(data, labels=keys)
plt.show()
