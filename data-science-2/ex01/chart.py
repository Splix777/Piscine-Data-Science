import sys
import os
import dotenv
import tqdm

import matplotlib.pyplot as plt

from datetime import datetime, timedelta, date
from matplotlib.dates import MonthLocator, DayLocator

from warehouse.database_connection import DatabaseConnection


def display_chart(count):
    # Check if dates are already in datetime.date format
    if isinstance(next(iter(count.keys())), date):
        dates = list(count.keys())
    else:
        # Convert string dates to datetime objects
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in count.keys()]

    # Plotting the data
    plt.plot(dates, count.values())

    # Set x-axis format based on the number of unique months
    unique_months = {date.strftime('%Y-%m') for date in dates}
    if len(unique_months) > 1:
        # If more than one month, display ticks at the beginning of each month
        plt.gca().xaxis.set_major_locator(MonthLocator())
        plt.gcf().autofmt_xdate()
    else:
        # If only one month, display ticks for each day
        plt.gca().xaxis.set_major_locator(DayLocator())

    # Set chart title and labels
    plt.title("Purchases from October 2022 to February 2023")
    plt.xlabel("Date")
    plt.ylabel("Purchases")

    # Show the plot
    plt.show()


def main():
    """
    Connects to the database and retrieves the data.
    Keeps only the "purchase" data of "event_type" column.
    Then creates 3 charts from the beginning of October 2022 to the end of February 2023.
    """
    dotenv.load_dotenv()
    with (DatabaseConnection(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            name=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
    ) as db):
        day = datetime(2022, 10, 1)
        count = {}

        # From the beginning of October 2022 to the end of February 2023
        total = (datetime(2023, 3, 1) - day).days
        with tqdm.tqdm(
                total=total,
                file=sys.stdout,
                desc="Creating charts",
                colour="green",
        ) as pbar:
            query = (
                "SELECT DATE(event_time) AS purchase_date, COUNT(*) AS purchase_count "
                "FROM customer "
                "WHERE event_type = 'purchase' "
                "AND event_time >= %s "
                "GROUP BY purchase_date"
            )

            start_date = datetime(2022, 12, 1)
            result = db.execute(query, (start_date,))

            for row in result:
                purchase_date, purchase_count = row
                count[purchase_date] = purchase_count
                pbar.update(1)
                pbar.set_postfix_str(f'Date: {str(purchase_date)} Found: {purchase_count}')


            # query = (
            #     "SELECT COUNT(*) "
            #     "FROM customer "
            #     "WHERE event_type = 'purchase' "
            #     "AND DATE(event_time) = %s"
            # )
            # while day < datetime(2022, 12, 1):
            #     result = db.execute(query, (day,))
            #     count[day.date()] = result[0]
            #     day += timedelta(days=1)
            #     pbar.update(1)
            #     pbar.set_postfix_str(f'Date: {str(day.date())} Found: {result[0][0]}')

        display_chart(count)


if __name__ == "__main__":
    main()
