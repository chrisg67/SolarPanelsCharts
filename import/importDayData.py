import sqlite3
import smacsv
import sys
import time
import glob

def main():
  files = glob.glob('olddata/d*.csv')
  conn = sqlite3.connect('..\\dB\\test.db')
  for f in files:
    y = f[9:13]
    m = f[13:15]
    d = f[15:17]
    date = y+'-'+m+'-'+d
    print date
    cmd = 'SELECT complete FROM day_data WHERE date = "%s";' % date
    print cmd
    result = conn.execute(cmd).fetchone()
    print result
    if result is None or result[0] != 1:
      data = smacsv.readDayFile(f)
      for val in data:
        cmd = "INSERT INTO five_minute_data VALUES ('" +  \
            time.strftime('%Y-%m-%d %H:%M:%S', val[0]) + "', " + \
            str(val[1]) + ", " + \
            str(val[2]) + ", " + \
            str(val[2]/12.0) + ");"
        print cmd
        conn.execute(cmd)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  
