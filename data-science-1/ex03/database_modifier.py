import io
import tqdm

from csv_info import CSVInfo
from database_connection import DatabaseConnection


def _get_data_types(column: str, data_type: str) -> str:
    """
    Takes a column and data type and returns the
    PostgreSQL data type.

    Args:
    column: str
    data_type: str

    Returns:
    str
    """
    csv_to_postgres_types = {
        "event_time": "TIMESTAMP",
        "event_type": "VARCHAR(255)",
        "product_id": "INTEGER",
        "price": "FLOAT",
        "user_id": "INTEGER",
        "user_session": "VARCHAR(255)",
        "category_id": "BIGINT",
        "category_code": "VARCHAR(255)",
        "brand": "VARCHAR(255)",
    }
    return csv_to_postgres_types[column]


class DatabaseModifier:
    """
    A class to create a table in a PostgreSQL database.

    Attributes:
    db: DatabaseConnection

    Methods:
    create_table: None
    """
    def __init__(self, database: DatabaseConnection):
        self.db = database

    def create_tables_from_csv(self, csv: CSVInfo):
        """
        Takes a .csv file and creates a table in the
        database for each file.

        Args:
        csv: CSVInfo
        """
        try:
            table_name = csv.filename.split(".")[0]
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            for column, data_type in csv.types.items():
                postgres_data_type = _get_data_types(str(column), data_type)
                query += f"{column} {postgres_data_type}, "
            query = query.rstrip(', ')  # Remove the trailing comma
            query += ")"
            self.db.execute(query)
        except Exception as e:
            print(f'Error in create_tables_from_csv: {e}')

    def load_csv_into_table(self, csv: CSVInfo, table_name: str = None):
        """
        Takes a .csv file and loads it into a table in the
        database.

        Args:
        csv: CSVInfo
        """
        try:
            if not table_name:
                table_name = csv.filename.split(".")[0]

            # Open the CSV file using a with statement
            with open(csv.full_path, 'r') as file:
                # Read the contents of the file
                file_contents = file.read()

                # Use io.StringIO to create a file-like object
                file_like_object = io.StringIO(file_contents)

                # Execute the COPY command with the file-like object
                query = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER;"
                self.db.cursor.copy_expert(sql=query, file=file_like_object)
                self.db.connection.commit()

        except Exception as e:
            print(f'Error in load_csv_into_table: {e}')

    def merge_existing_tables_to_one(self, tables: list, name: str = None):
        """
        Takes a list of tables and creates a single
        table named 'name' in the database. Merging the
        files into one table. If no name is given, we
        will return an error.

        Args:
        tables: list
        name: str
        """
        try:
            if not name:
                raise ValueError("Please provide a name for the table.")
            query = f"CREATE TABLE IF NOT EXISTS {name} AS ("
            for table in tqdm.tqdm(tables, desc="Creating table"):
                query += f"SELECT * FROM {table} UNION ALL "
            query = query.rstrip('UNION ALL ')  # Remove the trailing UNION ALL
            query += ")"
            self.db.execute(query)

        except Exception as e:
            print(f'Error in merge_existing_tables_to_one: {e}')

    def drop_table(self, table_name: str):
        """
        Drops a table from the database.

        Args:
        table_name: str
        """
        try:
            query = f"DROP TABLE IF EXISTS {table_name}"
            self.db.execute(query)
        except Exception as e:
            print(f'Error in drop_table: {e}')

    def remove_duplicates(self, table_name: str):
        """
        Removes duplicates from a table in the database.

        Args:
        table_name: str
        """
        try:
            query = (
                f"CREATE TEMPORARY TABLE temp_{table_name} AS "
                f"SELECT DISTINCT * FROM {table_name}; "
                f"TRUNCATE {table_name}; "
                f"INSERT INTO {table_name} SELECT * FROM temp_{table_name};"
            )
            self.db.execute(query)

        except Exception as e:
            print(f'Error in remove_duplicates: {e}')

    def join_tables(self, table1: str, table2: str, common_column: str):
        """
        Joins two tables together updating table1.
        table2 will remain unchanged.

        Args:
        - table1 (str): Name of the first table.
        - table2 (str): Name of the second table.
        - common_column (str): Common column used for the INNER JOIN.
        """
        try:
            query = (
                f"SELECT {table1}.*, {table2}.* "
                f"FROM {table1} "
                f"INNER JOIN {table2} "
                f"ON {table1}.{common_column} = {table2}.{common_column};"
            )
            self.db.execute(query)

        except Exception as e:
            print(f'Error in join_tables: {e}')

