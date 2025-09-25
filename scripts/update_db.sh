#!/bin/bash

# The first argument to this script should be the path to python executable.
# This is because when executed by the runner, it is unable to run the correct
# python executable from the virtual environment due to path issues. Hence
# a workaround is to explicitly provide the path.
# This script takes a date (formatted as YYYY-MM-DD) as the second argument and then
# executes the python batch load_ticker_data.py to insert data from the
# datafile for that date into the artha.db database.
# This will be called from a github actions workflow on a schedule.
#
echo "Running command: .venv/bin/python src/artha_data/batch/load_ticker_data.py $1"
.venv/bin/python src/artha_data/batch/load_ticker_data.py $1
echo "Exit status: $?"
exit $?
