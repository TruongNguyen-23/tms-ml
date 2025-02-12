from typing import Union
import pandas as pd
import sqlite3
import json
import os

class DataLoader:
    def __init__(self, data_dir: str = "Data/"):
        self.data_dir = data_dir

    def load_csv(self, filename: str) -> pd.DataFrame:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filename}' does not exist {self.data_dir}")
        
        df = pd.read_csv(filepath)
        return df

    def load_excel(self, filename: str) -> pd.DataFrame:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filename}' does not exist {self.data_dir}")
        
        df = pd.read_excel(filepath)
        return df

    def load_json(self, filename: str) -> pd.DataFrame:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File '{filename}' does not exist {self.data_dir}")
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        return df

    def load_sqlite(self, db_name: str, query: str) -> pd.DataFrame:
        db_path = os.path.join(self.data_dir, db_name)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database '{db_name}' does not exist {self.data_dir}")
        
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    

