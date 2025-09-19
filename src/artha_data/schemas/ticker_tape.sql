-- The ticker_tape table holds summary pricing data downloaded daily from NASDAQ with the US Stock Symbols datafiles

CREATE TABLE IF NOT EXISTS ticker_tape (
    load_date DATE,
    symbol TEXT,
    lastsale REAL,
    netchange REAL,
    pctchange REAL,
    volume INTEGER,
    marketCap REAL,
    adv_dec INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, load_date),
    FOREIGN KEY (symbol) REFERENCES stock_master(symbol)
  )
