from pathlib import Path
from typing import Dict

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import Vertical
from textual.events import Key


class CsvCategorizer(App):
    CSS = """
    Screen {
        align: center middle;
    }

    ListView {
        width: 60%;
        height: 80%;
        border: round white;
    }
    """

    BINDINGS = [
        ("r", "mark_credit", "Mark as Credit"),
        ("u", "mark_current", "Mark as Current"),
        ("n", "next", "Next"),
        ("q", "quit", "Quit Without Saving"),
    ]

    def __init__(self):
        super().__init__()
        self.csv_files = list(Path(".").glob("*.csv"))
        self.categories: Dict[str, str] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        self.list_view = ListView()
        yield Vertical(self.list_view)
        yield Footer()

    def on_mount(self) -> None:
        for file in self.csv_files:
            self.list_view.append(ListItem(Label(file.name)))

    def _update_label(self, index: int):
        file_name = self.csv_files[index].name
        category = self.categories.get(file_name, "Uncategorized")
        item = self.list_view.children[index]
        item.query_one(Label).update(f"{file_name}  →  {category}")

    def action_mark_credit(self):
        if self.list_view.index is not None:
            file_name = self.csv_files[self.list_view.index].name
            self.categories[file_name] = "Credit"
            self._update_label(self.list_view.index)

    def action_mark_current(self):
        if self.list_view.index is not None:
            file_name = self.csv_files[self.list_view.index].name
            self.categories[file_name] = "Current"
            self._update_label(self.list_view.index)

    def action_next(self):
        # Return categorized results when exiting
        self.exit(result=self.categories)

    def on_key(self, event: Key):
        if event.key == "enter":
            full_result = {
                file.name: self.categories.get(file.name, "Uncategorized")
                for file in self.csv_files
            }
            self.exit(result=full_result)


if __name__ == "__main__":
    app = CsvCategorizer()
    result = app.run()

    print("\nReturned Data:")
    print(result)