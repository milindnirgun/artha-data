-- This table holds the daily pricing data dump from Yahoo or other sources
CREATE TABLE IF NOT EXISTS stock_prices (
    symbol VARCHAR,
    Date DATE,
    Open DOUBLE,
    High DOUBLE,
    Low DOUBLE,
    Close DOUBLE,
    Volume BIGINT,
    Dividends DOUBLE,
    "Stock Splits" DOUBLE,
    PRIMARY KEY (symbol, Date)
)
