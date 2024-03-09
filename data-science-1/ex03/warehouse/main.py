import os
import sys
import tqdm
import dotenv

from warehouse.csv_info import CSVInfo
from warehouse.utils import check_errors
from warehouse.load_from_dir import LoadFromDir
from warehouse.database_modifier import DatabaseModifier
from warehouse.database_connection import DatabaseConnection


@check_errors(on_off=True)
def main():
    dotenv.load_dotenv()
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    with DatabaseConnection(host, port, name, user, password) as db:
        print(f'Connected to {os.getenv("DB_NAME")} database, user {os.getenv("DB_USER")}.')
        customer_directory = os.getenv("CSV_DIRECTORY")
        print(f'Loading files from {customer_directory}...')
        with LoadFromDir(directory=customer_directory) as loader:
            modifier = DatabaseModifier(db)
            progress = tqdm.tqdm(loader.files, desc='Creating tables from CSV', file=sys.stdout)
            for file in range(len(loader.files)):
                csv = CSVInfo(loader.files[file])
                modifier.create_tables_from_csv(csv=csv)
                modifier.load_csv_into_table(csv=csv)
                progress.update(1)

            tables_to_merge = [
                table for table in loader.filenames
                if table.startswith('data_202')]

            print(f'\nMerging tables: {tables_to_merge}')
            modifier.merge_existing_tables_to_one(tables=tables_to_merge, name='customer')
            print('Removing duplicates from customer table...')
            modifier.remove_duplicates(table_name='customer')
            print('Joining table customer to table item on product_id...')
            modifier.join_tables(table1='customer', table2='item', common_column='product_id')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
