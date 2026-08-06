
from typing import List

from models import Transaction


def process_added_or_deleted_transaction(existing_transactions:List[Transaction], new_transactions:List[Transaction]) -> List[Transaction]:
  added_transaction = get_added_transactions(existing_transactions, new_transactions)
  deleted_transactions = get_deleted_transactions(existing_transactions, new_transactions)
  # print new or deleted transactions
  # input saying make changes to transactions

  # process_existing_transactions to add/delete transaction
  # Import to keep labels from the existing transactions
  return

def get_added_transactions(existing_transactions:List[Transaction], new_transactions:List[Transaction]) -> List[Transaction]:
  return # New transactions

def get_deleted_transactions(existing_transactions:List[Transaction], new_transactions:List[Transaction]) -> List[Transaction]:
  return # New transactions