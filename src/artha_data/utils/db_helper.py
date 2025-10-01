import logging
import os

import duckdb

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DbHelper:
    @staticmethod
    def get_connection(_file, db_file):
        # Always pass the __file__ as the first argument from the caller. This
        # will help this function to construct a robust, absolute path to the
        # database no matter where or whichever program it is called
        # The second argument is the actual database filename so the connection
        # is made to the requested database and this helper can be reused with
        # multiple databases.
        # This helper assumes the database always exists in a "data" directory
        # under the project root.
        try:
            _PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(_file), "..", "..", ".."))
            _DB_DIR = os.path.join(_PROJECT_ROOT, "data")
            # _DATAFILE_DIR = os.path.join(_PROJECT_ROOT, "datafiles")
            os.makedirs(_DB_DIR, exist_ok=True)  # Ensure the data directory exists
            DB_FILE = os.path.join(_DB_DIR, db_file)
            return duckdb.connect(database=DB_FILE, read_only=False)
        except duckdb.Error as e:
            logging.error(f"Error connecting to database: {e}")
            return None
