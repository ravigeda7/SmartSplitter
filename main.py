# main.py

from storage.sheets_storage import read_families, read_event_details, read_event_expenses
from expenses import calculate_event_balances

def display_event_report(event):
    print(f"\n=== {event['Event Name']} ({event['Date']}) ===")
    participant_ids = event['Participating Families']
    records = read_event_expenses(event['Event ID'])
    total, share, balances = calculate_event_balances(records, participant_ids)

    print(f"Total spent: £{total:.2f}")
    print(f"Each participant's share: £{share:.2f}\n")
    print("Settlement:")
    for fam_id, balance in balances.items():
        print(f"{fam_id}: {'RECEIVE' if balance>0 else 'PAY' if balance<0 else 'Settled'} £{abs(balance):.2f}")

if __name__ == "__main__":
    families = read_families()
    events = read_event_details()

    print("Available Events:")
    for idx, e in enumerate(events):
        print(f"{idx+1}. {e['Event Name']} ({e['Date']})")

    choice = int(input("Select event number: "))
    event = events[choice-1]
    display_event_report(event)
