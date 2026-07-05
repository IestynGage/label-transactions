from models import Transaction
import pandas as pd
from typing import Dict, List
import os

def parse_csv_files(csv_files:Dict[str, str]) -> List[Transaction]:
    """Parse a list of CSV files."""
    all_transactions: List[Transaction] = []

    for (file_name, file_type) in csv_files.items():
        transactions = load_transactions(file_name, file_type)
        all_transactions = all_transactions + transactions

    return all_transactions

def parse_excel(file_path: str) -> list[Transaction]:
    """
    Parse an Excel file and returns a list of Transaction objects.
    """
    if not os.path.exists(file_path):
        return []

    df = pd.read_excel(file_path)
    
    # Fill any empty (NaN) cells with empty strings/0 to avoid errors
    df['Date'] = df['Date'].fillna('')
    df['Description'] = df['Description'].fillna('')
    df['Value'] = df['Value'].fillna(0)
    df['Label'] = df['Label'].fillna('')

    transactions = []
    
    # Iterate over the rows of the DataFrame
    for _, row in df.iterrows():
        # Create a Transaction object for each row
        txn = Transaction(
            date=str(row['Date']),
            desc=str(row['Description']),
            value=float(row['Value']), 
            account_type="",      # Not in Excel headings, defaulting to empty
            label=str(row['Label']),
            transactionType=""    # Defaulting to empty per your instruction
        )
        transactions.append(txn)
        
    return transactions

def load_transactions(csv_path: str, account_type:str) -> List[Transaction]:
    # Read CSV
    df = pd.read_csv(csv_path)

    # Ensure expected columns exist
    required_columns = [
        "Date",
        "Type",
        "Description",
        "Value",
        "Balance",
        "Account Name",
        "Account Number",
    ]
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Optional: Clean and normalize
    # df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    transactions = []


    print(account_type)
    normalize_value =  -1 if account_type.lower().strip() == "credit" else 1
    print(normalize_value)
    for _, row in df.iterrows():
        transaction = Transaction(
            date=row["Date"],
            desc=row["Description"],
            value=row["Value"] * normalize_value,
            account_type=account_type,
            label="",
            transactionType=""
        )
        transactions.append(transaction)

    return transactions