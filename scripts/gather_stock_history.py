import yfinance as yf
from datetime import date

import matplotlib.pyplot as plt

from typing import List, Tuple, Union


def plot_price(
        price_list: List[float],
        c: str = 'g',
        figsize: Tuple[int, int] = (6, 4),
        fontsize: int = 14,
        title: Union[str, None] = None,
    ) -> None:
    '''
    Plots a list of prices over epochs and optionally saves the plot to a specified path.

    Args:
        price_list (List[float]): A list of price values to plot.
        c (str, optional): Color of the plot line. Defaults to 'g' (green).
        figsize (Tuple, optional): Size of the figure (width, height). Defaults to (6, 4).
        fontsize (int, optional): Font size of the plot title. Defaults to 14.
        title (Union[str, None], optional): Title of the plot. If None, defaults to 'Price'. Defaults to None.
        save_path (Optional[str], optional): Path to save the plot image. If None, the plot is not saved. Default is None.

    Returns:
        None: This function does not return anything. It displays a plot.
    '''
    if title is None:
        title = 'Price'

    plt.figure(figsize=figsize)

    plt.plot(range(len(price_list)), price_list, c=c, label=title)
    plt.title(title, fontsize=fontsize)

    plt.xlabel("Days")
    plt.ylabel("Price")

    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    plt.show()

# Get the Ticker of the stock I'm interested
ticker = yf.Ticker("MS")

# Get the stock history for a single year
history = ticker.history(start="2017-1-9", end=date(2024, 6, 20), interval="1d")

# Modifying the DataFrame
history.reset_index(inplace=True)
history["Date"] = history["Date"].apply(lambda d: d.date())
history = history[["Date", "Open", "High", "Low", "Close", "Volume"]]

# plot_price(history['Close'])

# Save the DataFrame into a CSV
history.to_csv("../datasets/stock_prices/MS.csv")
