# table_creator.py

import os
import psycopg2
import dotenv
from load_csv import load
from ft_tqdm import ft_tqdm


class DatabaseConnection:
    """
    A class to connect to a PostgreSQL database.

    Attributes:
    connection: psycopg2.extensions.connection
    cursor: psycopg2.extensions.cursor

    Methods:
    close: None
    execute: None
    fetchall: list
    """
    def __init__(self, host, port, name, user, password):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=name,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """
        Closes the cursor and connection to the database.
        """
        self.cursor.close()
        self.connection.close()

    def execute(self, make_query, params=None):
        """
        Executes a SQL query.

        Args:
        query: str
        """
        self.cursor.execute(make_query, params)
        self.connection.commit()


class TableModifier:
    """
    A class to create a table in a PostgreSQL database.

    Attributes:
    db: DatabaseConnection

    Methods:
    create_table: None
    """
    def __init__(self, database: DatabaseConnection):
        self.db = database

    def create_table(self, list_of_tables: list, columns: dict):
        """
        Takes a list of .cvs files and creates a table in the
        database for each file.

        Args:
        list_of_tables: list
        columns: dict
        """
        for t in list_of_tables:
            query = f"CREATE TABLE IF NOT EXISTS {t} (id SERIAL PRIMARY KEY"
            for column, data_type in columns.items():
                query += f", {column} {data_type}"
            query += ")"
            self.db.execute(query)


class GetCSVNames:
    """
    A class to get the names of all .csv files in a directory.
    Returns list of names with .csv stripped.

    Attributes:
    directory: str

    Methods:
    get_csv_names: list
    """
    def __init__(self, directory: str):
        self.directory = directory

    def get_csv_names(self):
        """
        Gets the names of all .csv files in a directory.

        Returns:
        list
        """
        return [
            file.split(".")[0]
            for file in os.listdir(self.directory)
            if file.endswith(".csv")
        ]


if __name__ == "__main__":
    dotenv.load_dotenv()
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    customer_csvs = GetCSVNames("../subject/customer")
    list_of_tables = customer_csvs.get_csv_names()
    items_csvs = GetCSVNames("../subject/item")

    print(f'Found the following .csv files: {list_of_tables}')

    with DatabaseConnection(host, port, name, user, password) as db:
        table_creator = TableModifier(db)
        table_creator.create_table(
            list_of_tables,
            {
                "event_time": "TIMESTAMP",
                "event_type": "VARCHAR(255)",
                "product_id": "INTEGER",
                "price": "FLOAT",
                "user_id": "INTEGER",
                "user_session": "VARCHAR(255)"
            }
        )

        # To test we will only insert the first 100 rows from each csv file
        for table in list_of_tables:
            data = load(f"../subject/customer/{table}.csv")
            for i in ft_tqdm(range(100)):
                db.execute(
                    f"INSERT INTO {table} "
                    f"(event_time, event_type, product_id, price, "
                    f"user_id, user_session) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        data["event_time"][i],  # datetime
                        str(data["event_type"][i]),  # Convert to string
                        int(data["product_id"][i]),  # Convert to Python int
                        float(data["price"][i]),  # Convert to Python float
                        int(data["user_id"][i]),  # Convert to Python int
                        str(data["user_session"][i])  # Convert to string
                    )
                )
            print(f"Inserted 100 rows into {table}")

    print("Data inserted successfully")
