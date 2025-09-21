# storage/sheets_storage.py

import gspread, json, os
from google.oauth2.service_account import Credentials
import streamlit as st

# Declare the Google Sheet name ONCE here
SPREADSHEET_NAME = "https://docs.google.com/spreadsheets/d/1qyLxf4WDh2J0GZcaUz1e7J36TRcqT2BM7tElwxEANFA"
SCOPES=["https://www.googleapis.com/auth/spreadsheets"]

# Check if we are in a Streamlit Cloud environment
def get_google_client():
     if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
         # Use Streamlit's secrets management
         creds_dict = st.secrets["gcp_service_account"]
         creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
     else:
         # Fallback to local credentials file for local development
         creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

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
