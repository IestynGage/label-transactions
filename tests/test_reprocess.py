import pytest

from reprocess import get_added_transactions, get_deleted_transactions
from utils import make_transaction


class TestGetAddedTransactions:
    
  def test_returns_new_transaction(self):
      existing = [
          make_transaction(
              date="2026-01-01",
              desc="Coffee",
              value=5,
              account_type="current",
          )
      ]

      new = [
          existing[0],
          make_transaction(
              date="2026-01-02",
              desc="Groceries",
              value=20,
              account_type="current",
          ),
      ]

      result = get_added_transactions(existing, new)

      assert result == [new[1]]


  def test_returns_empty_when_nothing_added(self):
      transaction = make_transaction()

      existing = [transaction]
      new = [transaction]

      result = get_added_transactions(existing, new)

      assert result == []


  def test_returns_multiple_new_transactions(self):
      existing = [
          make_transaction(
              desc="Coffee",
              value=5,
              account_type="current",
          )
      ]

      new_transaction_1 = make_transaction(
          desc="Groceries",
          value=20,
          account_type="current",
      )
      new_transaction_2 = make_transaction(
          desc="Restaurant",
          value=30,
          account_type="credit",
      )

      new = [
          existing[0],
          new_transaction_1,
          new_transaction_2,
      ]

      result = get_added_transactions(existing, new)

      assert result == [new_transaction_1, new_transaction_2]


  def test_uses_only_transaction_key_fields(self):
      existing = [
          make_transaction(
              date="2026-01-01",
              desc="Coffee",
              value=5,
              account_type="current",
              label="food",
              transactionType="purchase",
          )
      ]

      # Same date, desc, value and account_type, but different label/type.
      new_transaction = make_transaction(
          date="2026-01-01",
          desc="Coffee",
          value=5,
          account_type="current",
          label="drinks",
          transactionType="refund",
      )

      result = get_added_transactions(existing, [new_transaction])

      assert result == []

class TestGetDeletedTransaction():
    
  def test_returns_removed_transaction(self):
      deleted = make_transaction(
          date="2026-01-01",
          desc="Coffee",
          value=5,
          account_type="current",
      )

      existing = [deleted]
      new = []

      result = get_deleted_transactions(existing, new)

      assert result == [deleted]


  def test_returns_empty_when_nothing_deleted(self):
    transaction = make_transaction()

    existing = [transaction]
    new = [transaction]

    result = get_deleted_transactions(existing, new)

    assert result == []

  def test_returns_multiple_deleted_transactions(self):
      deleted_1 = make_transaction(
          date="2026-01-01",
          desc="Coffee",
          value=5,
          account_type="current",
      )
      deleted_2 = make_transaction(
          date="2026-01-02",
          desc="Groceries",
          value=20,
          account_type="current",
      )
      remaining = make_transaction(
          date="2026-01-03",
          desc="Restaurant",
          value=30,
          account_type="credit",
      )

      existing = [deleted_1, deleted_2, remaining]
      new = [remaining]

      result = get_deleted_transactions(existing, new)

      assert result == [deleted_1, deleted_2]

  def test_does_not_return_new_transactions(self):
      existing = [
          make_transaction(
              date="2026-01-01",
              desc="Coffee",
              value=5,
              account_type="current",
          )
      ]

      new_transaction = make_transaction(
          date="2026-01-02",
          desc="Groceries",
          value=20,
          account_type="current",
      )

      new = [existing[0], new_transaction]

      result = get_deleted_transactions(existing, new)

      assert result == []

  def test_uses_transaction_key(self):
      existing_transaction = make_transaction(
          label="food",
          transactionType="purchase",
      )

      # Same transaction key, but different label and transaction type.
      new_transaction = make_transaction(
          label="drinks",
          transactionType="refund",
      )

      result = get_deleted_transactions(
          [existing_transaction],
          [new_transaction],
      )

      assert result == []