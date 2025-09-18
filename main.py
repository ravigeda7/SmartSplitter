# main.py

from expenses import calculate_balances
from storage.csv_storage import read_csv
from storage.sheets_storage import read_google_sheet

def show_report(records):
    total, share, balances = calculate_balances(records)

    print("\n--- Expense Report ---")
    print(f"Total spent: £{total:.2f}")
    print(f"Each family's share: £{share:.2f}\n")

    print("--- Settlement ---")
    for fam, balance in balances.items():
        if balance > 0:
            print(f"{fam} should RECEIVE £{balance:.2f}")
        elif balance < 0:
            print(f"{fam} should PAY £{-balance:.2f}")
        else:
            print(f"{fam} is settled.")

if __name__ == "__main__":
    print("=== Community Expense Splitter ===")

    # Choose data source
    source = input("Read from (1) CSV or (2) Google Sheets? ")

    if source == "1":
        filename = input("Enter CSV filename: ")
        records = read_csv(filename)
    else:
        sheet_name = input("Enter Google Sheet name: ")
        records = read_google_sheet(sheet_name)

    show_report(records)
