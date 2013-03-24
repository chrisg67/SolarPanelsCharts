import sqlite3
import sys

def main():
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  for year in range (2011, 2014):
    for month in range (1, 13):
      if ( not (year == 2011 and month < 11) ):
        for day in range (1, 32):
          date  = "%d-%02d-%02d" % (year, month, day)
          c.execute('SELECT complete FROM day_data WHERE date="'+date+'";')
          is_complete = c.fetchone()
          if is_complete is None or is_complete[0] == 0:
            where = "WHERE time BETWEEN '" + date + " 00:00:00' " + \
                    "AND '" + date + " 23:55:00';"
            sumd = "SELECT SUM(power_kWh) FROM five_minute_data " + where
            maxd = "SELECT MAX(total_power_kWh) FROM five_minute_data " + where
            count = "SELECT COUNT(power_kWh) FROM five_minute_data " + where
            c.execute(count)
            countv = c.fetchone()[0]
            if ( countv >= 200 ):
              # Complete day
              c.execute(sumd)
              sumv = c.fetchone()[0]
              c.execute(maxd)
              maxv = c.fetchone()[0]
              insert = "INSERT INTO day_data VALUES ('"+date+"', "+str(maxv)+", "+str(sumv)+", 1, NULL, NULL, 0);"
              print insert
              conn.execute(insert)
            else:
              print "incomplete day %s (%d)" % (date, countv)
          else:
            print "date is complete"
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  
