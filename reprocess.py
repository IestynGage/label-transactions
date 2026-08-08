
from typing import List

from models import Transaction

from typing import List

from models import Transaction


def transaction_key(transaction: Transaction):
    """Returns a unique identifier for a transaction."""
    return (
        transaction.date,
        transaction.desc,
        transaction.value,
        transaction.account_type,
    )


def get_added_transactions(
    existing_transactions: List[Transaction],
    new_transactions: List[Transaction],
) -> List[Transaction]:
    existing_keys = {transaction_key(t) for t in existing_transactions}

    return [
        t
        for t in new_transactions
        if transaction_key(t) not in existing_keys
    ]


def get_deleted_transactions(
    existing_transactions: List[Transaction],
    new_transactions: List[Transaction],
) -> List[Transaction]:
    new_keys = {transaction_key(t) for t in new_transactions}

    return [
        t
        for t in existing_transactions
        if transaction_key(t) not in new_keys
    ]


def process_added_or_deleted_transaction(
    existing_transactions: List[Transaction],
    new_transactions: List[Transaction],
) -> List[Transaction]:
    added_transactions = get_added_transactions(
        existing_transactions,
        new_transactions,
    )

    deleted_transactions = get_deleted_transactions(
        existing_transactions,
        new_transactions,
    )

    if added_transactions: 
        print(f"{len(added_transactions)} new transactions added")
        existing_transactions.extend(added_transactions)

    if deleted_transactions: 
        print("\nDeleted Transactions:")
        for transaction in deleted_transactions:
            print(transaction)

        if confirm_remove_deleted_transactions():
            for transaction in deleted_transactions:
                existing_transactions.remove(transaction)

    return existing_transactions


def confirm_remove_deleted_transactions() -> bool:
    while True:
        answer = input(
            "Do you wish to remove the deleted transactions? (y/n): "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y/yes or n/no.")

