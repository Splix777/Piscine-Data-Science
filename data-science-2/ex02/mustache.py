# Print the mean, median, min, max, first, second and third quartile of the price of
# the items purchased
# • Make box plots that display the price of the items purchased

import os
import dotenv

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime
from matplotlib.dates import MonthLocator, DayLocator, DateFormatter

from warehouse.database_connection import DatabaseConnection


def get_stats(prices: list) -> dict:
    """
    Returns the mean, median, min, max, first, second and third quartile of the price of the items purchased.

    Args:
    prices: list
    """
    return {
        "Count": len(prices),
        "Mean": sum(prices) / len(prices),
        "STD": np.std(prices),
        "Min": min(prices),
        "25%": sorted(prices)[len(prices) // 4],
        "50%": sorted(prices)[len(prices) // 2],
        "75%": sorted(prices)[len(prices) * 3 // 4],
        "Max": max(prices),
    }


def box_plot_by_price(prices: list) -> None:
    """
    Displays a box plot of the price of the items purchased

    Args:
    prices: list
    """
    fig, ax = plt.subplots()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.boxplot(
        prices,
        notch=True,
        vert=False,
        autorange=True,
        flierprops=dict(markersize=3),
    )

    # Set dynamic chart title and labels
    plt.title("Price of Items Purchased")
    plt.xlabel("Price")
    ax.set_yticks([tick for tick in ax.get_yticks() if tick != 1])
    ax.set_aspect('auto')
    plt.show()


def box_plot_by_quartiles(list_of_price_quartiles: list) -> None:
    """
    Displays a box plot of the price of the items purchased

    Args:
    list_of_price_quartiles: list
    """
    fig, ax = plt.subplots()
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.boxplot(
        list_of_price_quartiles,
        notch=True,
        vert=False,
        autorange=True,
        flierprops=dict(markersize=3),
    )

    # Set dynamic chart title and labels
    plt.title("Quartiles of the Price of Items Purchased")
    plt.xlabel("Price")
    ax.set_yticks([tick for tick in ax.get_yticks() if tick != 1])
    ax.set_aspect('auto')
    plt.show()


def make_box_plot(start_date: datetime, end_date: datetime, db: DatabaseConnection) -> None:
    """
    Connects to the database and retrieves the data.
    Displays a box plot of the price of the items purchased
    """
    query = """
    SELECT price
    FROM customer
    WHERE event_type = 'purchase'
    AND event_time BETWEEN %s AND %s
    """
    result = db.execute(query, (start_date, end_date))
    prices = [price[0] for price in result]

    price_distribution = get_stats(prices)
    for key, value in price_distribution.items():
        print(f"{key}: {value}")

    box_plot_by_price(prices)
    list_of_price_quartiles = [price_distribution["25%"], price_distribution["50%"], price_distribution["75%"]]
    box_plot_by_quartiles(list_of_price_quartiles)


def main():
    """
    Connects to the database and retrieves the data.
    Displays a box plot of the price of the items purchased
    """
    dotenv.load_dotenv()
    with DatabaseConnection(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            name=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
    ) as db:
        start_date = datetime(2022, 10, 1)
        end_date = datetime(2023, 3, 1)
        make_box_plot(start_date, end_date, db)


if __name__ == "__main__":
    main()