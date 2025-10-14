import streamlit as st
from storage.sheets_storage import read_families, read_event_details, read_event_expenses, append_expense
from expenses import calculate_event_balances
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Title + Slogan
st.title("⚖️ Our Community Expenses")

col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.markdown("### बराबर")
with col2: st.markdown("### సమ తుల్యం")
with col3: st.markdown("### ಸಮ ತೂಲ್ಯಂ")
with col4: st.markdown("### சம துல்யம்")
with col5: st.markdown("### ਸਮ ਤੁਲ੍ਯਮ੍")

# Load data
families = read_families()
family_map = {f['Family ID']: f['Family Name'] for f in families}
events = read_event_details()
event_names = [e['Event Name'] for e in events]

# --- Auto-select the open event ---
open_events = [e for e in events if e.get('Status', '').lower() == 'open']
default_event_name = open_events[0]['Event Name'] if open_events else event_names[0]

# Select Event (default = open one)
selected_event_name = st.selectbox("Select Event:", event_names, index=event_names.index(default_event_name))
event = next(e for e in events if e['Event Name'] == selected_event_name)
participant_ids = event['Participating Families']

# Load expenses safely
records = read_event_expenses(event['Event ID']) or []

# Prepare DataFrame to show Family Name instead of ID and remove Expense ID
if records:
    df_display = pd.DataFrame(records)
    if 'Family ID' in df_display.columns:
        df_display['Family'] = df_display['Family ID'].map(family_map)
        df_display = df_display[['Family', 'Description', 'Amount']]
    else:
        st.warning("No 'Family ID' column found in expenses sheet.")
else:
    df_display = pd.DataFrame(columns=['Family', 'Description', 'Amount'])

st.subheader("Expenses")
st.dataframe(df_display)

# Expense Form (only if event is Open)
if event['Status'].lower() == "open":
    st.subheader("➕ Add Expense")
    with st.form("expense_form", clear_on_submit=True):
        fam_choice = st.selectbox("Family", [family_map[fid] for fid in participant_ids])
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Map family name back to ID
            fam_id = [fid for fid, name in family_map.items() if name == fam_choice][0]
            append_expense(event['Event ID'], fam_id, description, amount)
            st.success("Expense added successfully! Please refresh to see it.")
else:
    st.info("This event is closed. You can only view the report.")

# Settlement Report
st.subheader("Report")
total, share, balances = calculate_event_balances(records, participant_ids)
st.write(f"**Total spent:** £{total:.2f}")
st.write(f"**Each participant's share:** £{share:.2f}")

st.subheader("Settlement")
for fam_id, balance in balances.items():
    fam_name = family_map.get(fam_id, fam_id)
    if balance > 0:
        st.success(f"{fam_name} should RECEIVE £{balance:.2f}")
    elif balance < 0:
        st.error(f"{fam_name} should PAY £{-balance:.2f}")
    else:
        st.info(f"{fam_name} is settled")
