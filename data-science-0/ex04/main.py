import os
import sys
import tqdm
import dotenv
import asyncio

from database_connection import DatabaseConnection
from load_from_dir import LoadFromDir
from csv_info import CSVInfo
from database_modifier import DatabaseModifier


async def load_tables_from_dir(db: DatabaseConnection, directory: str = None):
    print(f'Connected to {os.getenv("DB_NAME")} database, user {os.getenv("DB_USER")}.')

    modifier = DatabaseModifier(db)
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))
    files = LoadFromDir(directory=file_path)

    tasks = []
    start = asyncio.get_event_loop().time()

    for file in tqdm.tqdm(range(len(files.files)), desc="Creating tables", colour='green'):
        csv = CSVInfo(files.files[file])
        tasks.append(modifier.process_csv(csv))

    for task in tqdm.tqdm(range(len(tasks)), desc="Loading tables", colour='green'):
        await tasks[task]

    end = asyncio.get_event_loop().time()
    print(f"\nTime to create and load tables: {end - start:.2f} seconds.")


def main():
    try:
        dotenv.load_dotenv()
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        with DatabaseConnection(host, port, name, user, password) as db:
            asyncio.run(load_tables_from_dir(db, '../../subject'))
    except Exception as e:
        print(f'Error in main: {e}')


if __name__ == '__main__':
    main()
