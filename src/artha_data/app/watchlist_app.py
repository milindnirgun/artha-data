import os
import re

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, DataTable, Footer, Input, Label, Select

# Use below method of relative import by exporting PYTHONPATH=<...>/src and
# executing the program as a module with python -m artha_data.app.watchlist_app
from ..utils.watchlist_helper import WatchlistHelper


# --- Textual App ---
class WatchlistApp(App):
    """A Textual app to manage stock watchlists."""

    CSS_PATH = "watchlist_styles.css"
    symbols_to_delete = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Label("Manage Watchlists", classes="header")
        with Horizontal(id="new_watchlist_container", classes="row"):
            yield Input(placeholder="New Watchlist Name", id="new_watchlist_name")
            yield Button("Add Watchlist", id="add_watchlist")
        with Horizontal(id="watchlist_selection_container", classes="row"):
            yield Select([], id="watchlist_select", prompt="Select a Watchlist")
            yield Button("Delete", id="delete_watchlist", classes="red-button")
        with Horizontal(id="symbols_container", classes="row"):
            yield Input(placeholder="Stock Symbol(s) - comma or space separated", id="new_symbol")
            yield Button("+ Symbol(s)", id="add_symbol")
            yield Button("- Symbol(s)", id="delete_symbol", classes="red-button")
        yield DataTable(id="symbols_table", cursor_type="row")
        yield Footer()

    def _process_symbols(self, symbols_str: str) -> list[str]:
        """Processes a comma or space-separated string of symbols into a list of unique symbols."""
        return sorted(list(set([s.strip().upper() for s in re.split(r"[, ]+", symbols_str) if s.strip()])))

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.update_watchlist_select()
        table = self.query_one(DataTable)
        table.add_column("Symbol")

    def update_watchlist_select(self):
        """Updates the watchlist select widget with the latest data."""
        watchlist_select = self.query_one(Select)
        watchlists = WatchlistHelper.get_watchlists()
        watchlist_select.set_options([(wl[0], wl[0]) for wl in watchlists])

    def add_watchlist_handler(self) -> None:
        """Handles functionality for adding a new watchlist from the user
        input"""
        new_watchlist_name_input = self.query_one("#new_watchlist_name", Input)
        new_watchlist_name = new_watchlist_name_input.value
        if new_watchlist_name:
            if WatchlistHelper.watchlist_exists(new_watchlist_name):
                self.notify(f"Watchlist '{new_watchlist_name}' already exists.", title="Error", severity="error")
            else:
                WatchlistHelper.add_watchlist(new_watchlist_name)
                new_watchlist_name_input.value = ""
                self.update_watchlist_select()

    def add_symbols_handler(self) -> None:
        """Handles the adding of new symbols entered by the user in the Input
        field"""
        watchlist_select = self.query_one(Select)
        new_symbol_input = self.query_one("#new_symbol", Input)
        selected_watchlist = watchlist_select.value
        symbols_str = new_symbol_input.value
        if selected_watchlist and symbols_str:
            symbols = self._process_symbols(symbols_str)

            new_symbols = []
            duplicate_symbols = []

            for symbol in symbols:
                if WatchlistHelper.symbol_exists_in_watchlist(selected_watchlist, symbol):
                    duplicate_symbols.append(symbol)
                else:
                    new_symbols.append(symbol)

            if duplicate_symbols:
                self.notify(
                    f"Symbols already exist in watchlist: {', '.join(duplicate_symbols)}",
                    title="Error",
                    severity="error",
                )

            if new_symbols:
                for symbol in new_symbols:
                    WatchlistHelper.add_symbol_to_watchlist(selected_watchlist, symbol)
                self.notify(f"Added symbols: {', '.join(new_symbols)}")

            new_symbol_input.value = ""
            self.update_symbols_table(selected_watchlist)

    def delete_symbols_handler(self) -> None:
        """Handles the deletion of symbols entered by the user or selected in the table."""
        watchlist_select = self.query_one(Select)
        selected_watchlist = watchlist_select.value
        symbol_input = self.query_one("#new_symbol", Input)
        symbols_str = symbol_input.value

        if not selected_watchlist:
            self.notify("No watchlist selected.", title="Error", severity="error")
            return

        if self.symbols_to_delete:
            pass
        elif symbols_str:
            self.symbols_to_delete = self._process_symbols(symbols_str)
        else:
            self.notify("No symbols entered or selected for deletion.", title="Error", severity="error")
            return

        if not self.symbols_to_delete:
            self.notify("No symbols to delete.", title="Info", severity="information")
            return

        existent_symbols = []
        non_existent_symbols = []

        for symbol in self.symbols_to_delete:
            if WatchlistHelper.symbol_exists_in_watchlist(selected_watchlist, symbol):
                existent_symbols.append(symbol)
            else:
                non_existent_symbols.append(symbol)

        if non_existent_symbols:
            self.notify(
                f"Symbols not found in watchlist: {', '.join(non_existent_symbols)}",
                title="Error",
                severity="error",
            )

        if existent_symbols:
            WatchlistHelper.delete_symbols_from_watchlist(selected_watchlist, existent_symbols)
            self.notify(f"Deleted symbols: {', '.join(existent_symbols)}")
            self.symbols_to_delete.clear()
        symbol_input.value = ""
        self.update_symbols_table(selected_watchlist)

    def delete_watchlist_handler(self) -> None:
        """Handles deletion of select watchlist"""
        watchlist_select = self.query_one(Select)
        selected_watchlist = watchlist_select.value
        if selected_watchlist:
            WatchlistHelper.delete_symbols_from_watchlist(selected_watchlist)
            WatchlistHelper.delete_watchlist(selected_watchlist)
            # self.update_watchlist_select()
            self.query_one(DataTable).clear()
            self.notify(f"Watchlist '{selected_watchlist}' deleted.")
            watchlist_select.clear()
            self.update_watchlist_select()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "add_watchlist":
            self.add_watchlist_handler()
        elif event.button.id == "add_symbol":
            self.add_symbols_handler()
        elif event.button.id == "delete_symbol":
            self.delete_symbols_handler()
        elif event.button.id == "delete_watchlist":
            self.delete_watchlist_handler()

    async def on_select_changed(self, event: Select.Changed) -> None:
        """Event handler called when the select value changes."""
        if event.value != Select.BLANK:  # this is after a watchlist is deleted
            # db update is called only when the event value has a valid watchlist
            # name and not the deleted one
            self.update_symbols_table(event.value)

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """
        Event handler called when a row in the datatable is selected. This
        handler appends the class variable symbols_to_delete with the selected
        symbol. Each click appends to the list.
        TODO - implement multiple row selection.
        """
        data_table = self.query_one(DataTable)
        selected_row_key = event.row_key
        row_data = data_table.get_row(selected_row_key)
        for s in row_data:
            self.symbols_to_delete.append(s)

    def update_symbols_table(self, watchlist_name):
        """Updates the symbols table with data for the given watchlist."""
        table = self.query_one(DataTable)
        table.clear()
        if watchlist_name:
            symbols = WatchlistHelper.get_symbols_for_watchlist(watchlist_name)
            for symbol in symbols:
                table.add_row(symbol[0])


if __name__ == "__main__":
    app = WatchlistApp()
    app.run()
