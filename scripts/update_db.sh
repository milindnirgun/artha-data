#!/bin/bash

# This script takes a date (formatted as YYYY-MM-DD) as the first argument and then
# executes the python batch load_ticker_data.py to insert data from the
# datafile for that date into the artha.db database.
# This will be called from a github actions workflow on a schedule.
#
echo "Running command: python src/artha_data/batch/load_ticker_data.py $1"
python src/artha_data/batch/load_ticker_data.py $1
echo "Exit status: $?"
exit $?
