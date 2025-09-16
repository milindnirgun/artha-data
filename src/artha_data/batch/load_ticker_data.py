import json
import os
import sys
from datetime import datetime

import duckdb

# Construct a robust, absolute path to the database file.
# This assumes the script is in 'src/artha-data' and the db is in 'data/' at the project root.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_DB_DIR = os.path.join(_PROJECT_ROOT, "data")
_DATAFILE_DIR = os.path.join(_PROJECT_ROOT, "datafiles")
os.makedirs(_DB_DIR, exist_ok=True)  # Ensure the data directory exists
DB_FILE = os.path.join(_DB_DIR, "artha.db")


# 08/28/25 - This will read data from each of the exchange data files and insert into the ticker_tape table with the load_date specified
# It also updates/inserts the stock_master table with the other (non-price) information
def clean_value(value, value_type):
    """
    Cleans and converts a string value to a specified numeric type.

    Args:
        value: The input value, typically a string.
        value_type: The target type ('real' for float, 'integer' for int).

    Returns:
        The converted numeric value, or None if conversion fails or input is empty.
    """
    if value is None or value == "":
        return None
    try:
        if value_type == "real":
            return float(value.replace("$", "").replace("%", ""))
        if value_type == "integer":
            # Handle potential float strings like '123.0'
            return int(float(value))
    except (ValueError, TypeError):
        return None
    return value


def load_ticker_tape_data(con, load_date, data):
    """
    Loads time-sensitive ticker data into the ticker_tape table.

    Args:
        con: Active DuckDB connection.
        load_date: The specific date for which the data is being loaded.
        data: A list of dictionaries, where each dictionary is a stock's data.
    """
    for item in data:
        try:
            con.execute(
                """
                INSERT INTO ticker_tape (
                    load_date, symbol, lastsale, netchange, pctchange, volume, marketCap, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW(), NOW())
                """,
                (
                    load_date,
                    item.get("symbol"),
                    clean_value(item.get("lastsale"), "real"),
                    clean_value(item.get("netchange"), "real"),
                    clean_value(item.get("pctchange"), "real"),
                    clean_value(item.get("volume"), "integer"),
                    clean_value(item.get("marketCap"), "real"),
                ),
            )
        except (duckdb.ConstraintException, duckdb.ConversionException, ValueError) as e:
            print(f"Skipping row for symbol {item.get('symbol')} due to error: {e}")
            continue


def load_stock_master_data(con, data, exchange):
    """
    Inserts or updates records in the stock_master table with general stock info.

    This function is idempotent, using an ON CONFLICT clause to update existing
    stock symbols and insert new ones.

    Args:
        con: Active DuckDB connection.
        data: A list of dictionaries, where each dictionary is a stock's data.
        exchange: The stock exchange name (e.g., 'NASDAQ').
    """
    for item in data:
        try:
            # Get ipoyear and handle potential None values before converting to string
            ipoyear_val = item.get("ipoyear")
            ipoyear_str = str(ipoyear_val) if ipoyear_val not in [None, ""] else None

            con.execute(
                """
                INSERT INTO stock_master (symbol, name, ipoyear, nd_industry, nd_sector, exchange)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (symbol) DO UPDATE SET
                    name = excluded.name,
                    ipoyear = excluded.ipoyear,
                    nd_industry = excluded.nd_industry,
                    nd_sector = excluded.nd_sector,
                    exchange = excluded.exchange
                """,
                (item.get("symbol"), item.get("name"), ipoyear_str, item.get("industry"), item.get("sector"), exchange),
            )
        except duckdb.Error as e:
            print(f"Skipping master data for symbol {item.get('symbol')} due to error: {e}")
            continue


def load_data(con, load_date, datafile, exchange):
    """
    Orchestrates the loading of data from a single JSON file.

    It reads the file, then calls functions to load both the time-series
    price data (ticker_tape) and the general stock information (stock_master).

    Args:
        con: Active DuckDB connection.
        load_date: The load date for the data.
        datafile: Path to the JSON data file.
        exchange: The stock exchange name.
    Raises:
        ValueError
    """
    json_path = datafile

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        # First load the stock master table as it is a foreign key in the
        # ticker_tape table
        print(f"Loading stock master data from {os.path.basename(datafile)}...")
        load_stock_master_data(con, data, exchange)

        print(f"Loading ticker tape data from {os.path.basename(datafile)}...")
        load_ticker_tape_data(con, load_date, data)

        con.commit()
    except FileNotFoundError:
        raise ValueError(f"Warning: Data file not found at {json_path}. Skipping.")
    except json.JSONDecodeError:
        raise ValueError(f"Warning: Could not decode JSON from {json_path}. Skipping.")


def main() -> int:
    """
    Main entry point for the data loading script.

    Parses command-line arguments for the load date, connects to the database,
    and iterates through the exchange data files to load them.
    """
    rc = 0

    if len(sys.argv) < 2:
        print("Usage: python load_ticker_data.py YYYY-MM-DD")
        rc = 1
        return rc

    try:
        load_date_str = sys.argv[1]
        # Validate date format
        datetime.strptime(load_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        rc = 2
        return rc

    con = duckdb.connect(database=DB_FILE, read_only=False)

    # create_table(con)
    # Load data for all three exchanges
    nasdaq_file = _DATAFILE_DIR + "/nasdaq/nasdaq_full_tickers-" + load_date_str + ".json"
    amex_file = _DATAFILE_DIR + "/amex/amex_full_tickers-" + load_date_str + ".json"
    nyse_file = _DATAFILE_DIR + "/nyse/nyse_full_tickers-" + load_date_str + ".json"

    try:
        load_data(con, load_date_str, nasdaq_file, "NASDAQ")

        load_data(con, load_date_str, amex_file, "AMEX")

        load_data(con, load_date_str, nyse_file, "NYSE")

        con.close()
        print(f"Successfully loaded data for date: {load_date_str}")
    except (duckdb.Error, ValueError):
        print(f"Data load was unsuccessful for date: {load_date_str}")
        rc = -1

    return rc


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
