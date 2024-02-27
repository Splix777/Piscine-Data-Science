import io
import os
import tqdm
import sys
import dotenv

from database_connection import DatabaseConnection
from load_from_dir import LoadFromDir
from csv_info import CSVInfo


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

    def _get_data_types(self, column: str, data_type: str) -> str:
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
            "category_id": "INTEGER",
            "category_code": "VARCHAR(255)",
            "brand": "VARCHAR(255)",
        }
        postgres_data_type = csv_to_postgres_types[column]
        return postgres_data_type

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
                postgres_data_type = self._get_data_types(column, data_type)
                query += f"{column} {postgres_data_type}, "
            query = query.rstrip(', ')  # Remove the trailing comma
            query += ")"
            self.db.execute(query)
        except Exception as e:
            raise f'Error in create_tables_from_csv: {e}'

    def load_csv_into_table(self, csv: CSVInfo):
        try:
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
            raise f'Error in load_csv_into_table: {e}'


if __name__ == "__main__":
    try:
        dotenv.load_dotenv()
        with DatabaseConnection(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            name=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        ) as db:
            print(f'Connected to {os.getenv("DB_NAME")} database, user {os.getenv("DB_USER")}.')

            modifier = DatabaseModifier(db)
            files = LoadFromDir(
                directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '../subject')),
                file_extension="csv",
                multiple_subdirectories=True,
            )
            print(f"\nCreating tables for CSV in {files.directory}.")

            for file in tqdm.tqdm(
                    range(len(files.files)),
                    desc='Creating tables',
                    colour='green',
                    file=sys.stdout,
            ):
                csv = CSVInfo(files.files[file])
                modifier.create_tables_from_csv(csv)
                modifier.load_csv_into_table(csv)

    except Exception as e:
        print(f'Error in main: {e}')

