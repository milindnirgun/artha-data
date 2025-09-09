import json
import os
import sys
import unittest
from unittest.mock import MagicMock, mock_open, patch

import duckdb

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from artha_data.batch.load_ticker_data import (
    clean_value,
    load_data,
    load_stock_master_data,
    load_ticker_tape_data,
    main,
)


class TestLoadTickerData(unittest.TestCase):
    def test_clean_value(self):
        self.assertEqual(clean_value("123.45", "real"), 123.45)
        self.assertEqual(clean_value("$123.45", "real"), 123.45)
        self.assertEqual(clean_value("10%", "real"), 10.0)
        self.assertEqual(clean_value("123", "integer"), 123)
        self.assertEqual(clean_value("123.0", "integer"), 123)
        self.assertIsNone(clean_value(None, "real"))
        self.assertIsNone(clean_value("", "integer"))
        self.assertIsNone(clean_value("abc", "real"))
        self.assertIsNone(clean_value("abc", "integer"))
        self.assertIs(clean_value("test string", "str"), "test string")

    def setUp(self):
        self.con = duckdb.connect(":memory:")
        self.con.execute("""
            CREATE TABLE stock_master (
                symbol VARCHAR PRIMARY KEY,
                name VARCHAR,
                ipoyear VARCHAR,
                nd_industry VARCHAR,
                nd_sector VARCHAR,
                exchange VARCHAR
            );
        """)
        self.con.execute("""
            CREATE TABLE ticker_tape (
                load_date DATE,
                symbol VARCHAR,
                lastsale DOUBLE,
                netchange DOUBLE,
                pctchange DOUBLE,
                volume BIGINT,
                marketCap DOUBLE,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            );
        """)
        self.sample_data = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "lastsale": "150.00",
                "netchange": "2.50",
                "pctchange": "1.69%",
                "volume": "1000000",
                "marketCap": "2.5T",
                "ipoyear": "1980",
                "industry": "Technology",
                "sector": "Electronic Technology",
            }
        ]

    def tearDown(self):
        self.con.close()

    def test_load_stock_master_data(self):
        load_stock_master_data(self.con, self.sample_data, "NASDAQ")
        result = self.con.execute("SELECT * FROM stock_master").fetchone()
        self.assertEqual(result[0], "AAPL")
        self.assertEqual(result[1], "Apple Inc.")
        self.assertEqual(result[2], "1980")

    def test_load_ticker_tape_data(self):
        # First, insert a dummy record into stock_master to satisfy the foreign key constraint
        self.con.execute("INSERT INTO stock_master (symbol) VALUES ('AAPL')")
        load_ticker_tape_data(self.con, "2025-09-09", self.sample_data)
        result = self.con.execute("SELECT * FROM ticker_tape").fetchone()
        self.assertEqual(result[1], "AAPL")
        self.assertEqual(result[2], 150.00)
        self.assertEqual(result[5], 1000000)
        # Load the same data again to thrown the unique constraint and test the exception
        # UPDATE - this did not work as expected. @FIXIT
        load_ticker_tape_data(self.con, "2025-09-09", self.sample_data)
        result = self.con.execute("SELECT * FROM ticker_tape").fetchone()
        self.assertEqual(result[1], "AAPL")
        self.assertEqual(result[2], 150.00)
        self.assertEqual(result[5], 1000000)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"symbol": "GOOG", "name": "Google LLC"}]))
    @patch("artha_data.batch.load_ticker_data.load_stock_master_data")
    @patch("artha_data.batch.load_ticker_data.load_ticker_tape_data")
    def test_load_data(self, mock_load_tape, mock_load_master, mock_file):
        load_data(self.con, "2025-09-09", "dummy_path.json", "NASDAQ")
        mock_load_master.assert_called_once()
        mock_load_tape.assert_called_once()

    @patch("sys.argv", ["load_ticker_data.py", "2025-09-09"])
    @patch("artha_data.batch.load_ticker_data.duckdb.connect")
    @patch("artha_data.batch.load_ticker_data.load_data")
    def test_main(self, mock_load_data, mock_connect):
        mock_con = MagicMock()
        mock_connect.return_value = mock_con
        main()
        self.assertEqual(mock_load_data.call_count, 3)
        mock_con.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
