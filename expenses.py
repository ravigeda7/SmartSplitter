# expenses.py

from collections import defaultdict

def calculate_balances(records):
    """
    Takes a list of expense records (dicts with Family and Amount)
    Returns total, share, balances
    """
    expenses = defaultdict(float)

    for row in records:
        family = row["Family"]
        amount = float(row["Amount"])
        expenses[family] += amount

    families = len(expenses)
    total = sum(expenses.values())
    share = total / families if families > 0 else 0
    balances = {fam: paid - share for fam, paid in expenses.items()}

    return total, share, balances
