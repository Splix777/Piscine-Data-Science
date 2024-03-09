
import os
import dotenv

from warehouse.database_connection import DatabaseConnection
from warehouse.utils import check_errors
import matplotlib.pyplot as plt


def display_pie_chart(event_types: dict) -> None:
    """
    Display a pie chart of the event types.

    Args:
        event_types: A dictionary of event types and their counts.
    """
    plt.pie(
        event_types.values(),
        labels=event_types.keys(),
        autopct='%1.1f%%',
        startangle=170,
    )
    plt.show()

@check_errors(on_off=True)
def main():
    """
    Connect to the database and display a pie chart of the event types.
    """
    dotenv.load_dotenv()
    with DatabaseConnection(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            name=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
    ) as db:
        customer = 'customer'
        event_types = db.execute(f"SELECT event_type, COUNT(*) FROM {customer} GROUP BY event_type;")
        event_types = dict(event_types)
        display_pie_chart(event_types)


if __name__ == "__main__":
    main()
