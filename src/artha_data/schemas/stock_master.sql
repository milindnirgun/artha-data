-- This table holds the master data for all stocks being tracked. It has company relevant information and 
-- not the daily transient data. There are 3 types of industry/sector columns used to store the differences
-- between those values based on NASDAQ, Yahoo or FinViz classifications of a particular stock's industry
-- and sector.
CREATE TABLE IF NOT EXISTS stock_master (
  symbol TEXT,
  name TEXT,
  ipoyear TEXT,
  nd_industry TEXT,
  nd_sector TEXT,
  yh_industry TEXT,
  yh_sector TEXT,
  fz_industry TEXT,
  fz_sector TEXT,
  exchange TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (symbol)
)
