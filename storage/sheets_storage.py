# storage/sheets_storage.py

import gspread
from google.oauth2.service_account import Credentials

def read_google_sheet(sheet_name, credentials_file="credentials.json"):
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_name).sheet1
    return sheet.get_all_records()
