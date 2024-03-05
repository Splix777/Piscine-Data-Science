import io
import asyncio

from csv_info import CSVInfo
from database_connection import DatabaseConnection


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

    @staticmethod
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
            "event_time": "timestamp NOT NULL",
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

    async def create_tables_from_csv(self, csv: CSVInfo):
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
                postgres_data_type = self._get_data_types(str(column), data_type)
                query += f"{column} {postgres_data_type}, "
            query = query.rstrip(', ')  # Remove the trailing comma
            query += ")"
            self.db.execute(query)
        except Exception as e:
            print(f'Error in create_tables_from_csv: {e}')

    async def load_csv_into_table(self, csv: CSVInfo):
        try:
            table_name = csv.filename.split(".")[0]
            with open(csv.full_path, 'r') as file:
                file_contents = file.read()

                # Use io.StringIO to create a file-like object
                file_like_object = io.StringIO(file_contents)

                # Execute the COPY command with the file-like object
                query = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER;"
                self.db.cursor.copy_expert(sql=query, file=file_like_object)
                self.db.connection.commit()

        except Exception as e:
            print(f'Error in load_csv_into_table: {e}')

    async def process_csv(self, csv):
        await self.create_tables_from_csv(csv)
        await self.load_csv_into_table(csv)