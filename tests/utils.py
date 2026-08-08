from models import Transaction

def make_transaction(
    date="2026-01-01",
    desc="Coffee",
    value=5,
    account_type="current",
    label="food",
    transactionType="",
):
    transaction = Transaction(
        date,
        desc,
        value,
        account_type,
        label,
        transactionType,
    )
    transaction.account_type = account_type
    return transaction