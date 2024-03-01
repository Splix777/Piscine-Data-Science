import os
import pandas as pd


class CSVInfo:
    def __init__(self, filename):
        """
        A class to get information about a .csv file.

        Attributes:
        filename: str
        data: pd.DataFrame
        full_path: str
        list_of_columns: list
        columns: int
        types: pd.Series
        rows: int
        size: int
        """
        self.filename = filename.split("/")[-1]
        self.data = None
        self.full_path = filename
        self.list_of_columns = None
        self.columns = None
        self.types = None
        self.rows = None
        self.size = None
        self.get_info()

    def get_info(self):
        self.data = pd.read_csv(self.full_path)
        self.list_of_columns = list(self.data.columns)
        self.columns = len(self.data.columns)
        self.types = self.data.dtypes
        self.rows = len(self.data)
        self.size = os.path.getsize(self.full_path)

    def print_info(self):
        print(f"File: {self.filename}")
        print(f"Full path: {self.full_path}")
        print(f"Columns: {self.columns}")
        print(f"Types: {self.types}")
        print(f"Rows: {self.rows}")
        print(f"Size: {self.size} bytes")
        print("\n")
