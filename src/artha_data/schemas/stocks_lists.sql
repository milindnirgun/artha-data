-- This table is a joining table between watchlist and stock_master tables. 
CREATE TABLE IF NOT EXISTS stocks_lists (
    watchlist TEXT,
    symbol TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (watchlist, symbol),
    FOREIGN KEY (watchlist) REFERENCES watchlist(name),
    FOREIGN KEY (symbol) REFERENCES stock_master(symbol)
)
