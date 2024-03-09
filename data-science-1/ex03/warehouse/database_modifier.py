import io

from csv_info import CSVInfo
from database_connection import DatabaseConnection
from utils import check_errors, timing_decorator, write_to_file


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

    @timing_decorator(msg="Creating Tables from CSV")
    @check_errors(on_off=True)
    def create_tables_from_csv(self, csv: CSVInfo) -> list or None:
        """
        Takes a .csv file and creates a table in the
        database for each file.

        Args:
        csv: CSVInfo
        """
        table_name = csv.filename
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in csv.list_of_columns:
            postgres_data_type = self._get_data_types(column=str(column))
            query += f"{column} {postgres_data_type}, "
        query = query.rstrip(', ')
        query += ")"
        return self.db.execute(query)

    @timing_decorator(msg="Loading CSV into Table")
    @check_errors(on_off=True)
    def load_csv_into_table(self, csv: CSVInfo, table_name: str = None):
        """
        Takes a .csv file and loads it into a table in the
        database.

        Args:
        csv: CSVInfo
        """
        if not table_name:
            table_name = csv.filename.split(".")[0]

        with open(csv.full_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()
            file_like_object = io.StringIO(file_contents)

            query = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER;"
            self.db.cursor.copy_expert(sql=query, file=file_like_object)
            self.db.connection.commit()

    @timing_decorator(msg="Merging Tables")
    @check_errors(on_off=True)
    def merge_existing_tables_to_one(self, tables: list, name: str = None) -> list or None:
        """
        Takes a list of tables and creates a single
        table named 'name' in the database. Merging the
        files into one table. If no name is given, we
        will return an error.

        Args:
        tables: list
        name: str
        """
        if not name or not tables:
            raise ValueError("Please provide a name for the table and a list of tables to merge.")

        if self.db.table_exists(name):
            self.db.execute(f"TRUNCATE {name}")
        query = f"CREATE TABLE IF NOT EXISTS {name} AS ("
        for table in tables:
            query += f"SELECT * FROM {table} UNION ALL "
        query = query.rstrip("UNION ALL ")  # Remove trailing "UNION ALL"
        query += ")"
        return self.db.execute(query)

    @timing_decorator(msg="Removing Duplicates")
    @check_errors(on_off=True)
    def remove_duplicates(self, table_name: str) -> list or None:
        total_rows = self.db.get_total_rows(table_name)
        print(f'Warning: {total_rows} rows in {table_name}. This may take a while.')
        warning = input("Do you want to continue? (y/n): ")
        if warning.lower() != 'y':
            return

        delete_query = f"""
            DELETE FROM {table_name} AS a
            WHERE EXISTS (
                SELECT 1
                FROM {table_name} as b
                WHERE a.ctid <> b.ctid
                AND a.product_id = b.product_id
                AND a.price = b.price
                AND a.user_id = b.user_id
                AND a.user_session = b.user_session
                AND ABS(EXTRACT(EPOCH FROM a.event_time - b.event_time)) <= 1
            )
            RETURNING *
        """

        print("Deleting rows...")
        result = self.db.execute(delete_query)
        print(f"Rows deleted: {len(result)}")
        result_string = '\n'.join([str(row) for row in result])
        write_to_file('deleted_rows.txt', result_string)
        return result

    @timing_decorator(msg="Joining tables")
    @check_errors(on_off=True)
    def join_tables(self, table1: str, table2: str, common_column: str) -> list or None:
        list_of_columns_t1 = self.db.get_columns(table1)
        list_of_columns_t2 = self.db.get_columns(table2)

        list_of_columns_to_insert = [column for column in list_of_columns_t2 if column not in list_of_columns_t1]
        print(f"You're about to add the following columns to {table1}: {list_of_columns_to_insert}!")
        warning = input("Do you want to continue? (y/n): ")
        if warning.lower() != 'y':
            return

        for column in list_of_columns_to_insert:
            postgres_data_type = self._get_data_types(str(column))
            query = f"ALTER TABLE {table1} ADD COLUMN {column} {postgres_data_type};"
            self.db.execute(query)

        list_of_columns_t2.remove(common_column)
        columns_to_add = [f"{column} = i.{column}" for column in list_of_columns_t2]

        join_query = f"""
            UPDATE {table1} c
            SET {', '.join(columns_to_add)}
            FROM {table2} i
            WHERE c.{common_column} = i.{common_column};
        """
        return self.db.execute(join_query)

        # query = (
        #     f"UPDATE {table1} c "
        #     f"SET "
        #     f"{', '.join(columns_to_add)} "
        #     f"FROM {table2} i "
        #     f"WHERE c.{common_column} = i.{common_column};"
        # )

