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
          c.execute('SELECT total_power_kWh FROM day_data WHERE date="'+date+'";')
          total_power_kWh = c.fetchone()
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
            if total_power_kWh is None:
              insert = "INSERT INTO day_data VALUES ('"+date+"', "+str(maxv)+", "+str(sumv)+", 1, NULL, NULL, 0);"
              print insert
              conn.execute(insert)
            elif total_power_kWh[0] != maxv:
              print total_power_kWh[0],maxv
              insert = 'UPDATE day_data SET total_power_kWh='+str(maxv)+', power_kWh='+str(sumv)+' WHERE date="'+date+'";'
              print insert
              conn.execute(insert)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  
