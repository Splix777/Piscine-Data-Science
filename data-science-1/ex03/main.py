import os
import sys
import tqdm
import dotenv

from database_connection import DatabaseConnection
from load_from_dir import LoadFromDir
from csv_info import CSVInfo
from database_modifier import DatabaseModifier


def main():
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
            directory = os.getenv("CSV_DIRECTORY")
            with LoadFromDir(directory=directory) as loader:
                csv_files = loader.get_csv_files_table_names()
                modifier = DatabaseModifier(db)
                print(f'Found {len(csv_files)} CSV files in the {directory}.')
                # modifier.merge_existing_tables_to_one(tables=csv_files, name='customer')
                # modifier.remove_duplicates(table_name='customer')
                modifier.join_tables_batch(table1='customer', table2='item', common_column='product_id')

    except Exception as e:
        print(f'Error in main: {e}')


if __name__ == '__main__':
    main()
