# app.py

import streamlit as st
from expenses import calculate_balances
from storage.csv_storage import read_csv, write_csv
from storage.sheets_storage import read_google_sheet

st.set_page_config(page_title="Community Expense Splitter", page_icon="💰")

st.title("💰 Community Expense Splitter")

# Choose source
source = st.radio("Select data source:", ["CSV", "Google Sheets"])

records = []

if source == "CSV":
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        records = df.to_dict(orient="records")

elif source == "Google Sheets":
    sheet_name = st.text_input("Enter Google Sheet name")
    if st.button("Load Sheet") and sheet_name:
        try:
            records = read_google_sheet(sheet_name)
        except Exception as e:
            st.error(f"Error loading sheet: {e}")

# Show results if we have data
if records:
    st.subheader("📊 Expenses")
    st.dataframe(records)

    total, share, balances = calculate_balances(records)

    st.subheader("📋 Expense Report")
    st.write(f"**Total spent:** £{total:.2f}")
    st.write(f"**Each family's share:** £{share:.2f}")

    st.subheader("💸 Settlement")
    for fam, balance in balances.items():
        if balance > 0:
            st.success(f"{fam} should RECEIVE £{balance:.2f}")
        elif balance < 0:
            st.error(f"{fam} should PAY £{-balance:.2f}")
        else:
            st.info(f"{fam} is settled.")
