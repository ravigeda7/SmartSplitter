# test_expenses.py

import pytest
from expenses import calculate_balances

def test_simple_split():
    # 3 families, A paid 200, B paid 100, C paid 0
    records = [
        {"Family": "A", "Description": "Groceries", "Amount": 200},
        {"Family": "B", "Description": "Snacks", "Amount": 100},
        {"Family": "C", "Description": "Nothing", "Amount": 0},
    ]
    total, share, balances = calculate_balances(records)

    assert total == 300
    assert share == 100
    assert balances["A"] == 100
    assert balances["B"] == 0
    assert balances["C"] == -100

def test_multiple_expenses_per_family():
    # Family A paid twice, B once
    records = [
        {"Family": "A", "Description": "Groceries", "Amount": 150},
        {"Family": "A", "Description": "Cutlery", "Amount": 50},
        {"Family": "B", "Description": "Hall", "Amount": 100},
    ]
    total, share, balances = calculate_balances(records)

    assert total == 300
    assert share == 150
    assert balances["A"] == 50
    assert balances["B"] == -50
