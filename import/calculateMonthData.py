import sqlite3
import sys

def main():
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  for year in range (2011, 2014):
    for month in range (1, 13):
      if ( not (year == 2011 and month < 11) ):
        date  = "'%d-%02d-01'" % (year, month)
        where = "WHERE date BETWEEN " + date + \
                " AND date("+date+",'+1 month', '-1 day');"
        sumd = "SELECT SUM(power_kWh) FROM day_data " + where
        maxd = "SELECT MAX(total_power_kWh) FROM day_data " + where
        count = "SELECT COUNT(power_kWh) FROM day_data " + where
        c.execute(count)
        countv = c.fetchone()[0]
        if ( countv > 0 ):
          # Complete Month
          c.execute(sumd)
          sumv = c.fetchone()[0]
          c.execute(maxd)
          maxv = c.fetchone()[0]
          insert = "INSERT INTO month_data VALUES ("+date+", "+str(maxv)+", "+str(sumv)+", 1);"
          if c.execute('SELECT * from month_data WHERE date='+date+';').fetchone() is not None:
            insert = 'UPDATE month_data SET total_power_kWh='+str(maxv)+',power_kWh='+str(sumv)+' WHERE date='+date+';'
          print insert
          conn.execute(insert)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  
