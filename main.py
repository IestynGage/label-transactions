from excel_connector import open_excel_file
from exporter import export_transactions
from models import Transaction
from parser import parse_csv_files, parse_excel

from rules import Rules, filter_by_month, validate_label
from tui.CSVCategorizer import CsvCategorizer
from tui.ExtracMonth import MonthSelectorApp
from tui.existing import continue_with_existing
from reprocess import process_added_or_deleted_transaction

def main():
    transactions:list[Transaction] = []
    existing_transactions:list[Transaction] = parse_excel('transactions.xlsx')
    validate_label()

    match continue_with_existing(existing_transactions):
        case 're-label':
            transactions = existing_transactions
        case 're-process':
            month = transactions[0].date.split()[1]
            csv_files = CsvCategorizer().run() # TODO add a way that looks at the previous transactions to figure out CSVs (somehow)
            processed_transactions = filter_by_month(csv_transactions, month)
            transactions = process_added_or_deleted_transaction(existing_transactions, processed_transactions)
        case 'new':
            csv_files = CsvCategorizer().run()
            month = MonthSelectorApp(csv_files).run().split()[0]
            csv_transactions = parse_csv_files(csv_files)
            transactions = filter_by_month(csv_transactions, month)
        case 'cancel':
            return;
    
    labeled_transactions = Rules().apply(transactions)
    export_transactions(labeled_transactions)
    open_excel_file()

if __name__ == "__main__":
    main()