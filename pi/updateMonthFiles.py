#!/usr/bin/python2
import smacsv
import time
import sys
import os

months = [ '01 - Jan', '02 - Feb', '03 - Mar', '04 - Apr', '05 - May', '06 - Jun',
           '07 - Jul', '08 - Aug', '09 - Sep', '10 - Oct', '11 - Nov', '12 - Dec' ]

def main():
  for month in months:
    if os.path.exists(month):
      month_data = []
      month_file = '13 Cow Lane-2012'+month.partition(' ')[0]+'.csv'
      dirList = os.listdir(month)
      dirList.sort()
      for fname in dirList:
        day_data = smacsv.readDayFile(os.path.join(month, fname))
        total = 0.0
        for v in day_data:
          total = total + float(v[2])/12.0;
        month_date = v[0]
        found = 0
        for v in month_data:
          if month_date.tm_mday == v[0].tm_mday and month_date.tm_year == v[0].tm_year and month_date.tm_mon == v[0].tm_mon:
            found = 1

        if found == 0:
          month_data.append((month_date, 0.0, round(total, 3)))

      if os.path.exists(month_file):
        os.remove(month_file)
      smacsv.writeMonthFile(month_file, month_data)

if __name__ == "__main__":
  main()
