# expenses.py

from collections import defaultdict

def calculate_event_balances(expense_records, participant_ids):
    """
    Calculate settlement for a single event.

    expense_records: list of dicts with keys ['Family ID', 'Description', 'Amount']
    participant_ids: list of Family IDs participating in the event
    """
    expenses = defaultdict(float)

    # Sum expenses only for participating families
    for row in expense_records:
        fam_id = row['Family ID']
        if fam_id in participant_ids:
            expenses[fam_id] += float(row['Amount'])

    families_count = len(participant_ids)
    total = sum(expenses.values())
    share = total / families_count if families_count else 0

    balances = {}
    for fam_id in participant_ids:
        paid = expenses.get(fam_id, 0)
        balances[fam_id] = paid - share

    return total, share, balances
