import psycopg2

from warehouse.utils import check_errors


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
    @check_errors(on_off=True)
    def __init__(self, host, port, name, user, password):

        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        self.supports_executemany = True

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

    def execute(self, query, params=None) -> list or None:
        """
        Executes a SQL query.
    
        Args:
        query: str
        
        Returns:
        list or None
        """
        result = None

        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall() or None
        except psycopg2.ProgrammingError:
            pass
        finally:
            self.connection.commit()

        return result

    def get_columns(self, table_name: str) -> list:
        """
        Returns the columns of a table.

        Args:
        table_name: str

        Returns:
        list
        """
        self.execute(f"SELECT * FROM {table_name} LIMIT 0")
        return [desc[0] for desc in self.cursor.description]

    def get_total_rows(self, table_name: str) -> int:
        """
        Returns the total number of rows in a table.

        Args:
        table_name: str

        Returns:
        int
        """
        total_rows = self.execute(f"SELECT COUNT(*) FROM {table_name}")
        return total_rows[0][0]

    def drop_table(self, table_name: str):
        """
        Drops a table from the database.

        Args:
        table_name: str
        """
        return self.execute(f"DROP TABLE IF EXISTS {table_name}")

    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the database.

        Args:
        table_name: str

        Returns:
        bool
        """
        return bool(self.execute(
            f"SELECT EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}');"))
