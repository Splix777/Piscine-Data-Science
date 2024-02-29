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

    def create_one_table_from_multiple_csv(self, csv_files: list, name: str = None):
        """
        Takes a list of .csv files and creates a single
        table named 'name' in the database. Merging the
        files into one table. If no name is given, we
        will return an error.

        Args:
        csv_files: list
        name: str
        """
        try:
            if not name:
                raise ValueError("Please provide a name for the table.")
            query = f"CREATE TABLE IF NOT EXISTS {name} ("
            for csv in tqdm.tqdm(csv_files, desc="Creating table"):
                csv = CSVInfo(csv)
                for column, data_type in csv.types.items():
                    postgres_data_type = _get_data_types(str(column), data_type)
                    query += f"{column} {postgres_data_type}, "
            query = query.rstrip(', ')  # Remove the trailing comma
            query += ")"
            self.db.execute(query)

            for csv in tqdm.tqdm(csv_files, desc="Loading data"):
                csv = CSVInfo(csv)
                self.load_csv_into_table(csv, table_name=name)

        except Exception as e:
            print(f'Error in create_one_table_from_multiple_csv: {e}')
#
# CREATE TABLE IF NOT EXISTS customers AS (
#     SELECT * FROM data_2022_oct
#     UNION ALL
#     SELECT * FROM data_2022_nov
#     UNION ALL
#     SELECT * FROM data_2022_dec
#     UNION ALL
#     SELECT * FROM data_2023_jan
#     UNION ALL
#     SELECT * FROM data_2023_feb
# );