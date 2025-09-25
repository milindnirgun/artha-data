import os

import duckdb

# Construct a robust, absolute path to the database file.
# This assumes the script is in 'src/artha-data' and the db is in 'data/' at the project root.
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
_DB_DIR = os.path.join(_PROJECT_ROOT, "data")
_DATAFILE_DIR = os.path.join(_PROJECT_ROOT, "datafiles")
os.makedirs(_DB_DIR, exist_ok=True)  # Ensure the data directory exists
DB_FILE = os.path.join(_DB_DIR, "artha.db")


con = duckdb.connect(database=DB_FILE, read_only=False)
con.execute("show tables")
con.close()
