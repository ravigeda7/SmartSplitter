import gspread
from google.oauth2.service_account import Credentials

# Authorize with service account
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file("/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Open the sheet (by name or URL)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1qyLxf4WDh2J0GZcaUz1e7J36TRcqT2BM7tElwxEANFA").sheet1

# Read all rows into list of dicts
data = sheet.get_all_records()
for row in data:
    print(row)
