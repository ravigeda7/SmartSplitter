# app.py

import streamlit as st
from storage.sheets_storage import read_families, read_event_details, read_event_expenses
from expenses import calculate_event_balances

st.title("⚖️ Glevum Green Indian Community Balance Sheet")

# Create 5 equal columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("### बराबर")   # Hindi
with col2:
    st.markdown("### సమ తుల్యం")  # Telugu
with col3:
    st.markdown("### ಸಮ ತೂಲ್ಯಂ")  # Kannada
with col4:
    st.markdown("### சம துல்யம்")  # Tamil
with col5:
    st.markdown("### ਸਮ ਤੁਲ੍ਯਮ੍")  # Punjabi

# --- Data Loading ---
families = read_families()
family_map = {f['Family ID']: f['Family Name'] for f in families}

events = read_event_details()
event_names = [e['Event Name'] for e in events]

# --- Event Selection ---
selected_event_name = st.selectbox("Select Event:", event_names)
event = next((e for e in events if e['Event Name'] == selected_event_name), None)

if event:
    # --- Data Processing ---
    # The 'Participating Families' key now directly contains a list of Family IDs.
    participant_ids = event.get('Participating Families', [])

    records = read_event_expenses(event['Event ID'])

    # --- Display Expenses ---
    st.subheader(f"Expenses for {selected_event_name}")
    if records:
        st.dataframe(records)
    else:
        st.info("No expense records found for this event.")

    # --- Calculation ---
    total, share, balances = calculate_event_balances(records, participant_ids)

    # --- Display Report ---
    st.subheader("Report")
    st.write(f"**Total spent:** £{total:.2f}")
    st.write(f"**Each participant's share:** £{share:.2f}")

    # --- Display Settlement ---
    st.subheader("Settlement")
    if not balances:
        st.info("No balances to settle.")
    else:
        for fam_id, balance in balances.items():
            fam_name = family_map.get(fam_id, "Unknown Family")
            if balance > 0:
                st.success(f"{fam_name} should RECEIVE £{balance:.2f}")
            elif balance < 0:
                st.error(f"{fam_name} should PAY £{-balance:.2f}")
            else:
                st.info(f"{fam_name} is settled")
else:
    st.warning("Please select an event.")
