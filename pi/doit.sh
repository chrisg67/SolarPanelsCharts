#!/bin/bash
set -x
set -e
DATE=`date +%Y-%m-%d`
DATE2=`date +%Y%m%d`
if [ `date +%Y` -ge 2013 ] ; then
  ./smatool -from "${DATE} 00:00:00" -to "${DATE} 23:55:00" --inverter 4000TL > output
  ./convert2csv.pl output
  ./drawDayChartV2.py "13 Cow Lane-${DATE2}.csv"
  ./dropbox_uploader.sh upload todayV2.html "Public/WebSite/SolarPanels/today.html"
fi
