# storage/sheets_storage.py

import gspread, json, os
from google.oauth2.service_account import Credentials

# Declare the Google Sheet name ONCE here
SPREADSHEET_NAME = "https://docs.google.com/spreadsheets/d/1qyLxf4WDh2J0GZcaUz1e7J36TRcqT2BM7tElwxEANFA"

# def get_google_client(credentials_file="credentials.json"):
#     scopes = ["https://www.googleapis.com/auth/spreadsheets"]
#     creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
#     client = gspread.authorize(creds)
#     return client

def get_google_client():
    creds_dict = json.loads(os.environ["STREAMLIT_CREDENTIALS_JSON"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    return client

def get_spreadsheet():
    """Return the spreadsheet object"""
    client = get_google_client()
    return client.open_by_url(SPREADSHEET_NAME)

def read_sheet(worksheet_name):
    """
    Reads all rows from a given worksheet (tab).
    Returns a list of dicts (keys = headers).
    """
    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(worksheet_name)
    return worksheet.get_all_records()

def read_families():
    return read_sheet("Families")

def read_event_details():
    raw = read_sheet("EventDetails")
    for row in raw:
        # Look for the key with the trailing space, as seen in the debug output.
        participating_families_str = row.get('Participating Families ')
        if participating_families_str and isinstance(participating_families_str, str):
            # The value is a comma-separated string of IDs. Split it and clean up.
            row['Participating Families'] = [pid.strip() for pid in participating_families_str.split(',')]
        else:
            # If not found, or if it's not a string, default to an empty list.
            row['Participating Families'] = []
    return raw

def read_event_details():
    raw = read_sheet("EventDetails")
    for row in raw:
        # Look for the key with the trailing space, as seen in the debug output.
        participating_families_str = row.get('Participating Families ')
        if participating_families_str and isinstance(participating_families_str, str):
            # The value is a comma-separated string of IDs. Split it and clean up.
            row['Participating Families'] = [pid.strip() for pid in participating_families_str.split(',')]
        else:
            # If not found, or if it's not a string, default to an empty list.
            row['Participating Families'] = []
        row['Status'] = row.get('Status', 'Closed')  # Default to Closed if missing
    return raw


def read_event_expenses(event_id):
    return read_sheet(event_id)   # expects each event tab named by Event ID, e.g., "E01"

def append_expense(event_id, family_id, description, amount):
    """
    Append a new expense to a specific event sheet.

    event_id: str, e.g., "E01"
    family_id: str, e.g., "F01"
    description: str
    amount: float
    """
    records = read_event_expenses(event_id)
    new_expense_id = f"EX{len(records)+1:03}"  # auto-increment ID

    spreadsheet = get_spreadsheet()
    worksheet = spreadsheet.worksheet(event_id)
    worksheet.append_row([new_expense_id, family_id, description, amount])
