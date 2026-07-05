# Label Transaction

Labels CSV transaction.

## Scripts

```
uv run main.py # Label your transactions
uv run pytests # Run the tests
```

## How to label your transactions

You'll need two json files `income_labels.json` and `cost_labels.json`.
They'll need to define a label and be given a list of regexes.

```json
[
  {
    "label": "Salary",
    "regex": ["corefiling"]
  },
  ...
]
```

You'll also need the transaction files you which to label as well.

Once your ready run `uv run main.py`.
After running the program, and following it's instructions,
it will label the transactions and put them in a excel file.

If Excel is installed the file will be opened