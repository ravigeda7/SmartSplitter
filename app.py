import streamlit as st
from storage.sheets_storage import read_families, read_event_details, read_event_expenses, append_expense
from expenses import calculate_event_balances
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

# --- Find latest (open or closed) event ---
def get_latest_event(events, must_be_open=False):
    """Return the latest event (by numeric part of Event ID).
    If must_be_open=True, only consider open events."""
    filtered = [
        e for e in events
        if (not must_be_open or e.get("Status", "").lower() == "open")
    ]
    if not filtered:
        return None
    # Sort by numeric part of Event ID (e.g., E01 → 1, E12 → 12)
    return sorted(
        filtered,
        key=lambda e: int("".join(filter(str.isdigit, e.get("Event ID", "0"))))
    )[-1]

# Pick default event: latest open if exists, else latest overall
default_event = get_latest_event(events, must_be_open=True) or get_latest_event(events)
default_event_name = default_event["Event Name"]

# Select Event (default = latest open or latest overall)
selected_event_name = st.selectbox(
    "Select Event:",
    event_names,
    index=event_names.index(default_event_name)
)
event = next(e for e in events if e['Event Name'] == selected_event_name)
participant_ids = event['Participating Families']

# Load expenses safely
records = read_event_expenses(event['Event ID']) or []

# Prepare DataFrame
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
