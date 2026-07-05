import os
from typing import List, Dict, Any

from models import Transaction
import json
from pathlib import Path
import re

# Alternative solution is to create the file instead of error,
# then ask the user for the input.
def validate_label():
  if not os.path.exists("income_labels.json"):
    raise FileNotFoundError("Could not find income_labels.json")
  if not os.path.exists("cost_labels.json"):
    raise FileNotFoundError("Could not find cost_labels.json")


class Rules:

  def __init__(self):
      self.income_labels = self.load_labels("income_labels.json")
      self.cost_labels = self.load_labels("cost_labels.json")

#  TODO
  def load_labels(self, labels_file_json: str) -> List[Dict[str, Any]]:
    """
    Loads labels JSON.

    Expected format:
    [
      {
        "label": "Food",
        "regex": ["walmart", "wholefood"]
      }
    ]
    """

    path = Path(labels_file_json)

    if not path.exists():
        raise FileNotFoundError(f"{labels_file_json} not found")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data
  
  def apply(self, transactions: List[Transaction]):
    labeled_transactions = []

    for transaction in transactions:
      if transaction.label != "":
        labeled_transactions.append(transaction)
      elif transaction.value > 0:
        labeled_transactions.append(self.apply_label(transaction, self.income_labels))
      elif transaction.value < 1:
        labeled_transactions.append(self.apply_label(transaction, self.cost_labels))
      else:
        labeled_transactions.append(transaction)

    return labeled_transactions

  def apply_label(self, transaction, labels: List[Dict[str, Any]]):
    """
    Applies the first matching label rule to a transaction.
    """

    description = transaction.desc.lower()

    for rule in labels:
      label = rule["label"]
      patterns = rule["regex"]

      for pattern in patterns:
        if re.search(pattern, description):
          transaction.label = label
          return transaction

    return transaction
  
def filter_by_month(transactions: List[Transaction], month: str) -> List[Transaction]:
  """
  Filters a list of transactions by a 3-letter month string (e.g., 'jan', 'nov').
  Assumes transaction.date is in the format 'DD MMM YYYY'.
  """

  target_month = month.lower()

  filtered_transactions = []

  for t in transactions:
    try:
      if target_month in t.date.lower():
        filtered_transactions.append(t)

    except IndexError:
      continue

  return filtered_transactions