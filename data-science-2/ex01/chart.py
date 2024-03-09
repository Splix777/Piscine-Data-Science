import os
import dotenv

import matplotlib.pyplot as plt

from datetime import datetime
from matplotlib.dates import MonthLocator, DayLocator, DateFormatter

from warehouse.database_connection import DatabaseConnection


def display_line_graph(start_date: datetime, end_date: datetime, db: DatabaseConnection) -> None:
    """
    Connects to the database and retrieves the data.
    Displays a line graph of the number of customers per month
    """
    query = """
    SELECT DATE(event_time) AS purchase_date, COUNT(DISTINCT user_id) AS customer_count
    FROM customer
    WHERE event_type = 'purchase'
    AND event_time BETWEEN %s AND %s
    GROUP BY purchase_date
    """
    result = db.execute(query, (start_date, end_date))
    dates, counts = zip(*result)

    # Plotting the data
    plt.plot(dates, counts)

    # Simplified x-axis formatting
    set_x_axis_format(dates)

    # Set dynamic chart title and labels
    plt.title(f"Purchases from {start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}")
    plt.xlabel("Date")
    plt.ylabel("Number of Customers")

    # Show the plot
    plt.show()


def display_bar_graph(start_date: datetime, end_date: datetime, db: DatabaseConnection) -> None:
    """
    Connects to the database and retrieves the data.
    Displays a bar graph of the total sales in millions of dollars per month
    """
    query = """
    SELECT DATE(event_time) AS purchase_date, SUM(price) / 1000000 AS total_sales_millions
    FROM customer
    WHERE event_type = 'purchase'
    AND event_time BETWEEN %s AND %s
    GROUP BY purchase_date
    """
    result = db.execute(query, (start_date, end_date))
    dates, total_sales_millions = zip(*result)

    totals_per_month = {}
    for date, total in zip(dates, total_sales_millions):
        month = date.strftime('%Y-%m')
        if month in totals_per_month:
            totals_per_month[month] += total
        else:
            totals_per_month[month] = total

    dates = [datetime.strptime(month, '%Y-%m') for month in totals_per_month]
    total_sales_millions = list(totals_per_month.values())

    # Plotting the data as a bar graph
    plt.bar(dates, total_sales_millions, color='blue', width=20)

    # Simplified x-axis formatting
    set_x_axis_format(dates)

    # Set dynamic chart title and labels
    plt.title(f"Total Sales from {start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}")
    plt.xlabel("Date")
    plt.ylabel("Total Sales (Millions $)")

    # Show the plot
    plt.show()


def display_filled_line_graph(start_date: datetime, end_date: datetime, db: DatabaseConnection) -> None:
    """
    Connects to the database and retrieves the data.
    Displays a filled line graph of the average spending per customer in dollars per month
    """
    query = """
    SELECT DATE(event_time) AS purchase_month, 
           SUM(price) / COUNT(DISTINCT user_id) AS average_spending_per_customer
    FROM customer
    WHERE event_type = 'purchase'
    AND event_time BETWEEN %s AND %s
    GROUP BY purchase_month
    """
    result = db.execute(query, (start_date, end_date))
    months, average_spending_per_customer = zip(*result)

    # Plotting the data as a filled line graph
    plt.fill_between(months, 0, average_spending_per_customer, color='skyblue', alpha=0.2)
    plt.plot(months, average_spending_per_customer, color='blue', marker='')

    # Simplified x-axis formatting
    set_x_axis_format(months)

    # Set dynamic chart title and labels
    plt.title(f"Average Spending per Customer from {start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}")
    plt.xlabel("Month")
    plt.ylabel("Average Spending per Customer ($)")

    # Show the plot
    plt.show()


def set_x_axis_format(dates):
    unique_months = {date.strftime('%Y-%m') for date in dates}
    if len(unique_months) > 1:
        plt.gca().xaxis.set_major_locator(MonthLocator())
        plt.gca().xaxis.set_minor_locator(MonthLocator(bymonthday=15))
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))
    else:
        plt.gca().xaxis.set_major_locator(DayLocator())


def main():
    """
    Connects to the database and retrieves the data.
    Keeps only the "purchase" data of "event_type" column.
    Then creates 3 charts from the beginning of October 2022 to the end of February 2023.
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
        display_line_graph(start_date, end_date, db)
        display_bar_graph(start_date, end_date, db)
        display_filled_line_graph(start_date, end_date, db)


if __name__ == "__main__":
    main()
