import json
import pytest
from pathlib import Path

from rules import Rules
from models import Transaction


@pytest.fixture
def label_files(tmp_path, monkeypatch):
    """Create temporary label JSON files"""

    income = [
        {"regex": ["salary"], "label": "Income"},
        {"regex": ["bonus"], "label": "Bonus"},
    ]

    costs = [
        {"regex": ["coffee"], "label": "Food"},
        {"regex": ["uber"], "label": "Transport"},
    ]

    income_file = tmp_path / "income_labels.json"
    cost_file = tmp_path / "cost_labels.json"

    income_file.write_text(json.dumps(income))
    cost_file.write_text(json.dumps(costs))

    monkeypatch.chdir(tmp_path)

    return tmp_path


def test_load_labels(label_files):
    rules = Rules()

    assert rules.income_labels == [ 
        {
            "label": "Income",
            "regex" : [ "salary" ]
        },
        {
            "label": "Bonus",
            "regex" : [ "bonus" ]
        }
     ]

    assert rules.cost_labels == [ 
        {
            "label": "Food",
            "regex" : [ "coffee" ]
        },
        {
            "label": "Transport",
            "regex" : ["uber"]
        }
    ]


def test_load_labels_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError):
        Rules()


def test_apply_existing_label(label_files):
    rules = Rules()

    tx = Transaction(
        "2026-01-01",
        "salary payment",
        1000,
        "checking",
        "AlreadyTagged",
        "",
    )

    result = rules.apply([tx])

    assert result[0].label == "AlreadyTagged"


def test_apply_income_label(label_files):
    rules = Rules()

    tx = Transaction(
        "2026-01-01",
        "salary payment",
        1000,
        "checking",
        "",
        "",
    )

    result = rules.apply([tx])

    assert result[0].label == "Income"


def test_apply_cost_label(label_files):
    rules = Rules()

    tx = Transaction(
        "2026-01-01",
        "coffee shop",
        -5,
        "checking",
        "",
        "",
    )

    result = rules.apply([tx])

    assert result[0].label == "Food"


def test_apply_no_match(label_files):
    rules = Rules()

    tx = Transaction(
        "2026-01-01",
        "random purchase",
        -5,
        "checking",
        "",
        "",
    )

    result = rules.apply([tx])

    assert result[0].label == ""


def test_apply_zero_value_uses_cost_rules(label_files):
    rules = Rules()

    tx = Transaction(
        "2026-01-01",
        "uber trip",
        0,
        "checking",
        "",
        "",
    )

    result = rules.apply([tx])

    print(rules.cost_labels)
    assert result[0].label == "Transport"


def test_apply_label_first_match_wins(label_files):
    rules = Rules()

    rules.cost_labels =  [
        {'regex': ['coffee'], 'label': 'Food'}, 
        {'regex': ['coffee shop'], 'label': 'Cafe'}
    ]

    tx = Transaction(
        "2026-01-01",
        "coffee shop",
        -5,
        "checking",
        "",
        "",
    )

    result = rules.apply([tx])

    assert result[0].label == "Food"