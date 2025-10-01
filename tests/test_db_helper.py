import pytest
from artha_data.utils.DbHelper import DbHelper

def test_get_connection():
    """Tests that a database connection can be successfully established."""
    try:
        con = DbHelper.get_connection(__file__, "artha.db")
        result = con.execute("SELECT 1").fetchone()
        con.close()
        assert result == (1,)
    except Exception as e:
        pytest.fail(f"Database connection test failed with an exception: {e}")
