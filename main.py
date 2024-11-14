from cProfile import label

import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
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
    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(CSV.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print("No transactions are found in the giving date range")
        else:
            print(f"Transactions from {start_date.strftime("%d-%m-%Y")} to {end_date.strftime("%d-%m-%Y")}")

            print(filtered_df.to_string(index=False,
                                        formatters={"date":lambda x: x.strftime("%d-%m-%Y")}))
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\n Summary: ")
            print(f"total income : ${total_income:.2f}.")
            print(f"total expense : ${total_expense: .2f}")
            print(f"Net saving: ${(total_income-total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csvfile()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or hit enter for today's date: ")
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("date", inplace=True)
    df_income = (df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0))
    df_expense = (df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0))
    plt.figure(figsize=(10, 5))
    plt.plot(df_income.index, df_income["amount"], label="Income", color="g")
    plt.plot(df_expense.index, df_income["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Income and Expense (t)")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():

    while True:
        choice = input("1- add new transaction.\n2-view transactions and summary within a date range."
                       "\n3-Exit.\nPlease enter your activity: ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("enter start date (dd-mm-yyyy): ")
            end_date = get_date("enter end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see a plot ? (y/n)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting ... ")
            break
        else:
            print("Invalid choice please choose (1-2-3). ")



if __name__ == "__main__":
    main()
