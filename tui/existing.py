from typing import List

from models import Transaction


from typing import List, Literal

def continue_with_existing(transactions: List[Transaction]) -> Literal["re-label", "re-process", "new", "cancel"]:
    if not transactions:
        return "new"

    month = transactions[0].date.split()[1]
    total_transactions = len(transactions)
    transactions_with_label = sum(1 for t in transactions if t.label)

    print(f"\nFound {total_transactions} transactions for {month} ({transactions_with_label} labelled).")
    print("1. Add missing labels")
    print("2. Re-process csv transactions")
    print("3. Start fresh (New)")
    print("4. Cancel")
    
    user_choice = input("Select an option (1-4): ").strip()

    if user_choice == "1":
        return "re-label"
    elif user_choice == "2":
        return "re-process"
    elif user_choice == "3":
        return "new"
    else:
        return "cancel"
