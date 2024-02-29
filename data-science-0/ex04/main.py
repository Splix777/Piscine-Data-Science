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

            modifier = DatabaseModifier(db)
            files = LoadFromDir(
                directory=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../subject')),
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
                try:
                    modifier.create_tables_from_csv(csv)
                    modifier.load_csv_into_table(csv)
                except Exception as e:
                    print(f'Error in loading tables: {e}')

    except Exception as e:
        print(f'Error in main: {e}')


if __name__ == '__main__':
    main()
