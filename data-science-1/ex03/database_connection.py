import psycopg2


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
            raise e

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

    def get_columns(self, table_name):
        """
        Returns the columns of a table.

        Args:
        table_name: str

        Returns:
        list
        """
        self.execute(f"SELECT * FROM {table_name} LIMIT 0")
        return [desc[0] for desc in self.cursor.description]
