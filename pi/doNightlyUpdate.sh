#!/bin/bash
set -e
if [ `date +%Y` -ge 2013 ] ; then 
  ./grabAll.sh
  ./convertDayData.sh
  ./doCharts.sh
  ./uploadNightly.sh
fi
