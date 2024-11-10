import pandas as pd
import csv
from datetime import datetime

from data_entry import get_date, get_category, get_amount, get_description

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    @classmethod
    def initialize_csvfile(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            dataframe = pd.DataFrame(columns=cls.COLUMNS)
            dataframe.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description" : description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("entry added successfully")


def add():
    CSV.initialize_csvfile()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or hit enter for today's date: ")
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

add()