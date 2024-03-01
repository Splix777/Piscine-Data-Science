import io
import math

import tqdm

from csv_info import CSVInfo
from database_connection import DatabaseConnection


def _get_data_types(column: str) -> str:
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
        "event_time": "DATETIME",
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
                postgres_data_type = _get_data_types(str(column))
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

    def remove_duplicates(self, table_name: str, batch_size: int = 1000):
        """
        Removes duplicates from a table in the database.

        Args:
        table_name: str
        """
        try:
            query_total_rows = f"SELECT COUNT(*) FROM {table_name};"
            total_rows = self.db.execute(query_total_rows)[0]
            print(f'Total rows: {total_rows}')

            offset = 0

            with tqdm.tqdm(total=total_rows, desc="Removing Duplicates", unit="row") as pbar:
                while offset < total_rows:
                    query = (
                        f"CREATE TEMPORARY TABLE temp_{table_name} AS "
                        f"SELECT DISTINCT t1.* FROM {table_name} t1 "
                        f"WHERE NOT EXISTS ("
                        f"    SELECT 1 FROM {table_name} t2 "
                        f"    WHERE t1.event_type = t2.event_type "
                        f"      AND t1.product_id = t2.product_id "
                        f"      AND t1.price = t2.price "
                        f"      AND ABS(EXTRACT(MICROSECOND FROM AGE(t1.event_time, t2.event_time))) < 1000000"
                        f"      AND t1 <> t2"
                        f"); "
                        f"TRUNCATE {table_name}; "
                        f"INSERT INTO {table_name} SELECT * FROM temp_{table_name};"
                        f"LIMIT {batch_size} OFFSET {offset};"

                    )
                    self.db.execute(query)
                    offset += batch_size
                    pbar.update(batch_size)

        except Exception as e:
            print(f'Error in remove_duplicates: {e}')

    def join_tables_batch(self, table1: str, table2: str, common_column: str, batch_size: int = 1000):
        try:
            # Estimate total rows without fetching all rows
            query_total_rows = f"SELECT COUNT(*) FROM {table1};"
            total_rows = self.db.execute(query_total_rows)[0]
            print(f'Total rows: {total_rows}')

            offset = 0
            list_of_columns_t1 = self.db.get_columns(table1)
            list_of_columns_t2 = self.db.get_columns(table2)

            list_of_columns_to_insert = [column for column in list_of_columns_t2 if column not in list_of_columns_t1]

            for column in list_of_columns_to_insert:
                postgres_data_type = _get_data_types(str(column))
                query = f"ALTER TABLE {table1} ADD COLUMN {column} {postgres_data_type};"
                self.db.execute(query)

            list_of_columns_t2.remove(common_column)
            columns_to_add = [f"{column} = i.{column}" for column in list_of_columns_t2]
            print(f'Columns to add: {columns_to_add}')

            query = (
                f"UPDATE {table1} c "
                f"SET "
                f"{', '.join(columns_to_add)} "
                f"FROM {table2} i "
                f"WHERE c.{common_column} = i.{common_column};"
            )
            self.db.execute(query)
        except Exception as e:
            print(f'Error in join_tables_batch: {e}')
