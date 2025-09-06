from collections import defaultdict

def calculate_balances(expenses, families):
    """
    Calculate how much each family owes or should receive.
    """
    total = sum(expenses.values())
    share = total / families
    balances = {fam: paid - share for fam, paid in expenses.items()}
    return total, share, balances


if __name__ == "_main_":
    print("=== Community Expense Splitter (Multiple Expenses) ===\n")

    families = int(input("Enter number of families: "))
    expenses = defaultdict(float)

    # Collect expenses
    for i in range(families):
        name = input(f"\nEnter family {i+1} name: ")
        while True:
            desc = input(f"Enter expense description for {name} (or 'done' to finish): ")
            if desc.lower() == "done":
                break
            amount = float(input(f"  Amount for {desc}: £"))
            expenses[name] += amount

    # Process
    total, share, balances = calculate_balances(expenses, families)

    # Output results
    print("\n--- Expense Report ---")
    print(f"Total spent: £{total:.2f}")
    print(f"Each family's share: £{share:.2f}\n")

    print("--- Settlement ---")
    for fam, balance in balances.items():
        if balance > 0:
            print(f"{fam} should RECEIVE £{balance:.2f}")
        elif balance < 0:
            print(f"{fam} should PAY £{-balance:.2f}")
        else:
            print(f"{fam} is settled.")
