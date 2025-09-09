-- This table holds the names and description of watchlist or any categorization of symbols
CREATE TABLE IF NOT EXISTS watchlist (
    name TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (name)
)
