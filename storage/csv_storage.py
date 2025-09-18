# storage/csv_storage.py

import csv

def read_csv(filename):
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(filename, records):
    fieldnames = ["Family", "Description", "Amount"]
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
