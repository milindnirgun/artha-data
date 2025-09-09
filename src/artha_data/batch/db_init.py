import os
import sys

import duckdb

# Construct a robust, absolute path to the database file.
# This assumes the script is in 'src/artha-data' and the db is in 'data/' at the project root.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_DB_DIR = os.path.join(_PROJECT_ROOT, "data")
os.makedirs(_DB_DIR, exist_ok=True)  # Ensure the data directory exists
DB_FILE = os.path.join(_DB_DIR, "artha.db")
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "schemas")


def table_exists(connection: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    """
    Checks if a table exists in the DuckDB database.
    """
    try:
        result = connection.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name = ?", [table_name]
        ).fetchone()
        return result is not None
    except duckdb.Error as e:
        print(f"An error occurred checking table existence: {e}")
        return False


def create_table_from_schema(table_name: str):
    """
    Creates a table in the DuckDB database using a .sql schema file.
    """
    schema_file = os.path.join(SCHEMA_DIR, f"{table_name}.sql")

    if not os.path.exists(schema_file):
        print(f"Error: Schema file not found at '{schema_file}'")
        sys.exit(1)

    try:
        with open(schema_file, "r") as f:
            # Read all lines and filter out SQL comments (starting with '--') before executing
            schema_sql = "".join(line for line in f if not line.strip().startswith("--"))
    except IOError as e:
        print(f"Error reading schema file: {e}")
        sys.exit(1)

    try:
        con = duckdb.connect(database=DB_FILE, read_only=False)

        if table_exists(con, table_name):
            print(f"Table '{table_name}' already exists. Skipping creation.")
        else:
            print(f"Creating table '{table_name}' from '{os.path.basename(schema_file)}'...")
            con.execute(schema_sql)
            print(f"Table '{table_name}' created successfully.")

    except duckdb.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    finally:
        if "con" in locals():
            con.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/artha/db_init.py <table_name>")
        print("Available schemas:", [f.split(".")[0] for f in os.listdir(SCHEMA_DIR) if f.endswith(".sql")])
        sys.exit(1)

    table_to_create = sys.argv[1]
    create_table_from_schema(table_to_create)
