#!/usr/bin/python2
import csv
import time

class dialect(csv.excel):
  delimiter=';'

def readMonthFile(fname):
  reader = csv.reader(open(fname, 'r'), dialect=dialect)
  monthdata=[]
  for row in reader:
    if len(row)==3:
      try:
        t = time.strptime(row[0], "%d/%m/%Y")
        monthdata.append((t, float(row[1]), float(row[2])))
      except ValueError:
        pass
  return monthdata

def writeMonthFile(fname, monthdata):
  writer = csv.writer(open(fname, 'w'), dialect=dialect)
  monthdata.sort()
  for row in monthdata:
    t = time.strftime("%d/%m/%Y", row[0])
    writer.writerow([t, row[1], row[2]])

def readDayFile(fname):
  reader = csv.reader(open(fname, 'r'), dialect=dialect)
  daydata=[]
  for row in reader:
    if len(row)==3:
      try:
        t = time.strptime(row[0], "%d/%m/%Y %H:%M:%S")
        daydata.append((t, float(row[1]), float(row[2])))
      except ValueError:
        pass
  return daydata

def writeDayFile(fname, daydata):
  writer = csv.writer(open(fname, 'w'), dialect=dialect)
  daydata.sort()
  for row in daydata:
    t = time.strftime("%d/%m/%Y %H:%M:%S", row[0])
    writer.writerow([t, str(row[1]), str(int(row[2]))])

def main():
  m = readDayFile("13 Cow Lane-20120916.csv")
  writeDayFile("bananaday.csv", m)

if __name__ == "__main__":
  main()

  
