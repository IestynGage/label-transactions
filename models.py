class Transaction:
  def __init__(
      self, date: str, desc: str, value: int, account_type:str, label: str, transactionType: str
  ):
    self.date = date
    self.desc = desc
    self.value = value
    self.account_type = account_type
    self.label = label
    self.transactionType = transactionType  # empty string for now

  def __repr__(self):
    return f"Transaction(date={self.date}, desc={self.desc}, value={self.value}, label={self.label})"