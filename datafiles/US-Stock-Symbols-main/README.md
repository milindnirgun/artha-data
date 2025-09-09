# US-Stock-Symbols

An aggregation of current US Stock Symbols in `json` format.  This repo is modified from the original with the following differences:
- only store the "*_full_tickers.json" files and not create any of the other .txt redundant files.
- create a new file everyday with the date appended to the name
- TODO - write an action to purge older files and save storage

Updated at 6 pm PDT.
## Exchanges Available:
- NASDAQ
- NYSE
- AMEX


## How to use the data

Each exchange has a file named as 

`exchange_full_ticker-<date>.json` 

This is the raw data from NASDAQ list.  It contains the following data fields:
- Symbol
- Company/Name
- Last closing price for the day
- Net Change in price from previous close
- Percentage change in price from previous close
- Volume
- Market Capitalization
- Country
- IPO Year
- Industry
- Sector
- URL

