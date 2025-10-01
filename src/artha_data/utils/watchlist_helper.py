# Use below method of relative import by exporting PYTHONPATH=<...>/src and
# executing the program as a module with python -m artha_data.app.watchlist_app
from .db_helper import DbHelper

DB_FILE = "artha.db"


def get_db_connection():
    """Returns a connection to the DuckDb database named with global"""
    return DbHelper.get_connection(__file__, DB_FILE)


class WatchlistHelper:
    """Helper class with static methods for executing SQL queries for each function."""

    @staticmethod
    def add_watchlist(name, description=""):
        """Inserts a new row in the watchlist table with the name & description passed"""
        with get_db_connection() as con:
            con.execute("INSERT INTO watchlist (name, description) VALUES (?, ?)", (name, description))

    @staticmethod
    def get_watchlists():
        """Returns a list of ordered watchlists."""
        with get_db_connection() as con:
            return con.execute("SELECT name FROM watchlist ORDER BY name").fetchall()

    @staticmethod
    def watchlist_exists(name):
        """Checks if a watchlist with given name already exists (case insensitive)
        and returns True or False."""
        with get_db_connection() as con:
            result = con.execute("SELECT 1 FROM watchlist WHERE LOWER(name) = LOWER(?)", (name,)).fetchone()
            return result is not None

    @staticmethod
    def delete_watchlist(name):
        """Deletes a row from watchlist with the given name. This will leave
        orphan records in stocks_lists and other tables that have foreign keys
        to the watchlist table, therefore delete corresponding rows from all
        child tables first."""
        with get_db_connection() as con:
            con.execute("DELETE FROM watchlist WHERE name = ?", (name,))

    @staticmethod
    def delete_all_symbols_from_watchlist(watchlist_name):
        """Deletes all rows from stocks_lists table that are related to the
        given watchlist."""
        with get_db_connection() as con:
            con.execute("DELETE FROM stocks_lists WHERE watchlist = ?", (watchlist_name,))

    @staticmethod
    def add_symbol_to_watchlist(watchlist_name, symbol):
        """Inserts a row in stocks_lists table with the given symbol linking it
        to the given watchlist."""
        with get_db_connection() as con:
            con.execute("INSERT INTO stocks_lists (watchlist, symbol) VALUES (?, ?)", (watchlist_name, symbol))

    @staticmethod
    def delete_symbols_from_watchlist(watchlist_name, symbols: list[str]):
        with get_db_connection() as con:
            if not symbols:
                return
            con.execute("DELETE FROM stocks_lists WHERE watchlist = ? AND symbol IN ?", (watchlist_name, tuple(symbols)))

    @staticmethod
    def get_symbols_for_watchlist(watchlist_name):
        """Returns a list of symbols for a given watchlist."""
        with get_db_connection() as con:
            return con.execute(
                "SELECT symbol FROM stocks_lists WHERE watchlist = ? ORDER BY symbol", (watchlist_name,)
            ).fetchall()

    @staticmethod
    def symbol_exists_in_watchlist(watchlist_name, symbol):
        """Checks if any symbol exists for a given watchlist and returns True
        or False."""
        with get_db_connection() as con:
            result = con.execute(
                "SELECT 1 FROM stocks_lists WHERE watchlist = ? AND symbol = ?", (watchlist_name, symbol)
            ).fetchone()
            return result is not None
