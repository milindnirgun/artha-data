#/bin/bash

# Get date as YYYY-MM for the prior month
PRIOR_MONTH=$(date -d "1 month ago" +%Y-%m)

cd ./datafiles
zip -r amex_full_tickers-${PRIOR_MONTH}.zip amex/*$PRIOR_MONTH*
zip -r nasdaq_full_tickers-${PRIOR_MONTH}.zip nasdaq/*$PRIOR_MONTH*
zip -r nyse_full_tickers-${PRIOR_MONTH}.zip nyse/*$PRIOR_MONTH*

rm -fv amex/*$PRIOR_MONTH*
rm -fv nasdaq/*$PRIOR_MONTH*
rm -fv nyse/*$PRIOR_MONTH*

exit 0
