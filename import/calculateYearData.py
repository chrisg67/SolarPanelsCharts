import sqlite3
import sys

def main():
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  for year in range (2011, 2014):
    date  = "'%d-01-01'" % (year)
    where = "WHERE date BETWEEN " + date + \
            " AND date("+date+",'+1 year');"
    sumd = "SELECT SUM(power_kWh) FROM month_data " + where
    maxd = "SELECT MAX(total_power_kWh) FROM month_data " + where
    count = "SELECT COUNT(power_kWh) FROM month_data " + where
    c.execute(count)
    countv = c.fetchone()[0]
    if ( countv > 0 ):
      # Complete Year
      c.execute(sumd)
      sumv = c.fetchone()[0]
      c.execute(maxd)
      maxv = c.fetchone()[0]
      insert = "INSERT INTO year_data VALUES ("+date+", "+str(maxv)+", "+str(sumv)+", 1);"
      print insert
      conn.execute(insert)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  
