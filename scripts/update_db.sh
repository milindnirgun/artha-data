#!/bin/bash

# This script takes a date (formatted as YYYY-MM-DD) as a parameter and then
# executes the python batch load_ticker_data.py to insert data from the
# datafile for that date into the artha.db database.
# This will be called from a github actions workflow on a schedule.
#
python src/artha_data/batch/load_ticker_data.py $1
exit $?
