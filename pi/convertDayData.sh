#!/bin/bash
set -e
cd currentData/2013
../../convert2csv_fullDays.pl ../../fullOutput
../../updateMonthFiles.py

